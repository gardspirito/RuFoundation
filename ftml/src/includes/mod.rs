/*
 * includes/mod.rs
 *
 * ftml - Library to parse Wikidot text
 * Copyright (C) 2019-2022 Wikijump Team
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with this program. If not, see <http://www.gnu.org/licenses/>.
 */

//! This module implements "messy includes", or Wikidot native includes.
//!
//! It is an annoying but necessary hack that parses the psueodblock
//! `[[include-messy]]` and directly replaces that part with the
//! foreign page's wikitext.

mod include_ref;
mod includer;
mod parse;

pub use self::include_ref::IncludeRef;
pub use self::includer::{DebugIncluder, FetchedPage, Includer, NullIncluder};

use self::parse::parse_include_block;
use crate::data::PageRef;
use crate::settings::WikitextSettings;
use crate::tree::VariableMap;
use lazy_static::__Deref;
use regex::{Regex, RegexBuilder};

lazy_static! {
    static ref INCLUDE_REGEX: Regex = {
        RegexBuilder::new(r"^\[\[\s*include-messy\s+")
            .case_insensitive(true)
            .multi_line(true)
            .dot_matches_new_line(true)
            .build()
            .unwrap()
    };
    static ref INCLUDE_COMPAT_REGEX: Regex = {
        RegexBuilder::new(r"^\[\[\s*include\s+")
            .case_insensitive(true)
            .multi_line(true)
            .dot_matches_new_line(true)
            .build()
            .unwrap()
    };
    static ref NO_INCLUDE_REGEX: Regex = {
        RegexBuilder::new(r"^\[\[\s*noinclude\s*\]\]\s*\n(.*?)\n\[\[/\s*noinclude\s*\]\]\s*$")
            .case_insensitive(true)
            .multi_line(true)
            .dot_matches_new_line(true)
            .build()
            .unwrap()
    };
    static ref VARIABLE_REGEX: Regex =
        Regex::new(r"\{\$(?P<name>[a-zA-Z0-9_\-]+)\}").unwrap();
}

pub fn remove_noincludes<'t>(input: &'t str) -> String {
    let no_include_regex = NO_INCLUDE_REGEX.deref();
    let input_stripped_of_no_include = no_include_regex.replace_all(input, "${1}").to_owned();
    String::from(input_stripped_of_no_include)
}

pub fn include<'t, I, E, F>(
    input: &'t str,
    settings: &WikitextSettings,
    mut includer: I,
    invalid_return: F,
) -> Result<(String, Vec<PageRef<'t>>), E>
where
    I: Includer<'t, Error = E>,
    F: FnOnce() -> E,
{
    if !settings.enable_page_syntax {
        info!("Includes are disabled for this input, skipping");

        let output = str!(input);
        let pages = vec![];
        return Ok((output, pages));
    }

    info!("Finding and replacing all instances of include blocks in text");

    let mut ranges = Vec::new();
    let mut includes = Vec::new();

    let regex = if settings.use_include_compatibility { 
        INCLUDE_COMPAT_REGEX.deref()
    } else {
        INCLUDE_REGEX.deref()
    };

    let no_include_regex = NO_INCLUDE_REGEX.deref();

    // Get include references
    for mtch in regex.find_iter(input) {
        let start = mtch.start();

        debug!(
            "Found include regex match (start {}, slice '{}')",
            start,
            mtch.as_str(),
        );

        match parse_include_block(&input[start..], start, settings) {
            Ok((include, end)) => {
                ranges.push(start..end);
                includes.push(include.to_owned());
            }
            Err(_) => warn!("Unable to parse include regex match"),
        }
    }

    // Retrieve included pages
    let fetched_pages = includer.include_pages(&includes)?;

    // Ensure it matches up with the request
    if includes.len() != fetched_pages.len() {
        return Err(invalid_return());
    }

    // Substitute inclusions
    //
    // We must iterate backwards for all the indices to be valid

    let ranges_iter = ranges.into_iter();
    let includes_iter = includes.into_iter();
    let fetched_iter = fetched_pages.into_iter();

    let joined_iter = ranges_iter.zip(includes_iter).zip(fetched_iter).rev();

    // Borrowing from the original text and doing in-place insertions
    // will not work here. We are trying to both return the page names
    // (slices from the input string), and replace it with new content.
    let mut output = String::from(input);
    let mut pages = Vec::new();

    for ((range, include), fetched) in joined_iter {
        let (page_ref, variables) = include.into();

        info!(
            "Replacing range for included page ({}..{})",
            range.start, range.end,
        );

        // Ensure the returned page reference matches
        if page_ref != fetched.page_ref {
            return Err(invalid_return());
        }

        // Get replaced content, or error message
        let replace_with = match fetched.content {
            // Take fetched content, replace variables
            Some(mut content) => {
                replace_variables(content.to_mut(), &variables);
                content
            }

            // Include not found, return premade template
            None => includer.no_such_include(&page_ref)?,
        };

        let replace_with_no_includes = no_include_regex.replace_all(replace_with.as_ref(), "");

        // Append page to final list
        pages.push(page_ref);

        // Perform the substitution
        output.replace_range(range, &replace_with_no_includes);
    }

    // Since we iterate in reverse order, the pages are reversed.
    pages.reverse();

    // Return
    Ok((output, pages))
}

fn replace_variables(content: &mut String, variables: &VariableMap) {
    let mut matches = Vec::new();

    // Find all variables
    for capture in VARIABLE_REGEX.captures_iter(content) {
        let mtch = capture.get(0).unwrap();
        let name = &capture["name"];

        if let Some(value) = variables.get(name) {
            matches.push((value, mtch.range()));
        }
    }

    // Replace the variables
    // Iterates backwards so indices stay valid
    matches.reverse();
    for (value, range) in matches {
        content.replace_range(range, value);
    }
}