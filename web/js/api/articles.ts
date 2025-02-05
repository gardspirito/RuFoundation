import {wFetch} from "../util/fetch-util";
import {UserData} from "./user";
import {ModuleRateVotesResponse} from './rate'

export interface ArticleData {
    pageId: string
    title?: string
    source?: string
    tags?: Array<string>
    parent?: string
    locked?: boolean
}

export interface ArticleUpdateRequest extends ArticleData {
    forcePageId?: boolean
}

export async function createArticle(data: ArticleData) {
    await wFetch(`/api/articles/new`, {method: 'POST', sendJson: true, body: data});
}

export function fetchArticle(id: string): Promise<ArticleData> {
    return wFetch<ArticleData>(`/api/articles/${id}`);
}

export async function updateArticle(id: string, data: ArticleUpdateRequest): Promise<ArticleData> {
    return wFetch<ArticleData>(`/api/articles/${id}`, {method: 'PUT', sendJson: true, body: data});
}

export async function deleteArticle(id: string) {
    await wFetch(`/api/articles/${id}`, {method: 'DELETE', sendJson: true});
}

export interface ArticleLogEntry {
    revNumber: number
    user: UserData
    comment: string
    createdAt: string
    type: string
    meta: Record<string, any>
}

export interface ArticleLog {
    count: number
    entries: Array<ArticleLogEntry>
}

export async function fetchArticleLog(id: string, from: number = 0, to: number = from+25): Promise<ArticleLog> {
    return await wFetch<ArticleLog>(`/api/articles/${id}/log?from=${from}&to=${to}`)
}

export async function revertArticleRevision(id: string, revNumber: number): Promise<ArticleData> {
    return await wFetch(`/api/articles/${id}/log`, {method: 'PUT', sendJson: true, body: {revNumber: revNumber}})
}

export interface ArticleVersion {
    source: string
    rendered: string
}

export async function fetchArticleVersion(pageId: string, rev_num: number, pathParams?: { [key: string]: string }): Promise<ArticleVersion> {
    return await wFetch<ArticleVersion>(`/api/articles/${pageId}/version?revNum=${rev_num}&pathParams=${JSON.stringify(pathParams)}`)
}

export interface ArticleBacklink {
    id: string
    title: string
    exists: boolean
}

export interface ArticleBacklinks {
    children: Array<ArticleBacklink>
    includes: Array<ArticleBacklink>
    links: Array<ArticleBacklink>
}

export async function fetchArticleBacklinks(pageId: string): Promise<ArticleBacklinks> {
    return await wFetch<ArticleBacklinks>(`/api/articles/${pageId}/links`)
}

export async function fetchArticleVotes(pageId: string): Promise<ModuleRateVotesResponse> {
    return await wFetch<ModuleRateVotesResponse>(`/api/articles/${pageId}/votes`)
}

export async function deleteArticleVotes(pageId: string): Promise<ModuleRateVotesResponse> {
    return await wFetch<ModuleRateVotesResponse>(`/api/articles/${pageId}/votes`, { method: 'DELETE' })
}