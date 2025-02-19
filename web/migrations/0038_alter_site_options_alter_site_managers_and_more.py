# Generated by Django 5.1.4 on 2025-02-05 12:28

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0017_alter_user_visual_group'),
        ('web', '0037_vote_visual_group'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='site',
            options={'verbose_name': 'Сайт', 'verbose_name_plural': 'Сайты'},
        ),
        migrations.AlterModelManagers(
            name='site',
            managers=[
            ],
        ),
        migrations.RemoveConstraint(
            model_name='article',
            name='web_article_unique',
        ),
        migrations.RemoveConstraint(
            model_name='articlelogentry',
            name='web_articlelogentry_unique',
        ),
        migrations.RemoveConstraint(
            model_name='category',
            name='web_category_unique',
        ),
        migrations.RemoveConstraint(
            model_name='externallink',
            name='web_externallink_unique',
        ),
        migrations.RemoveConstraint(
            model_name='file',
            name='web_file_unique',
        ),
        migrations.RemoveConstraint(
            model_name='tag',
            name='web_tag_unique',
        ),
        migrations.RemoveConstraint(
            model_name='tagscategory',
            name='web_tagscategory_unique',
        ),
        migrations.RemoveConstraint(
            model_name='vote',
            name='web_vote_unique',
        ),
        migrations.RemoveField(
            model_name='article',
            name='site',
        ),
        migrations.RemoveField(
            model_name='articlelogentry',
            name='site',
        ),
        migrations.RemoveField(
            model_name='articleversion',
            name='site',
        ),
        migrations.RemoveField(
            model_name='category',
            name='site',
        ),
        migrations.RemoveField(
            model_name='externallink',
            name='site',
        ),
        migrations.RemoveField(
            model_name='file',
            name='site',
        ),
        migrations.RemoveField(
            model_name='forumcategory',
            name='site',
        ),
        migrations.RemoveField(
            model_name='forumpost',
            name='site',
        ),
        migrations.RemoveField(
            model_name='forumpostversion',
            name='site',
        ),
        migrations.RemoveField(
            model_name='forumsection',
            name='site',
        ),
        migrations.RemoveField(
            model_name='forumthread',
            name='site',
        ),
        migrations.RemoveField(
            model_name='tag',
            name='site',
        ),
        migrations.RemoveField(
            model_name='tagscategory',
            name='site',
        ),
        migrations.RemoveField(
            model_name='vote',
            name='site',
        ),
        migrations.AlterField(
            model_name='articlelogentry',
            name='type',
            field=models.TextField(choices=[('source', 'Source'), ('title', 'Title'), ('name', 'Name'), ('tags', 'Tags'), ('new', 'New'), ('parent', 'Parent'), ('file_added', 'Fileadded'), ('file_deleted', 'Filedeleted'), ('file_renamed', 'Filerenamed'), ('votes_deleted', 'Votesdeleted'), ('wikidot', 'Wikidot'), ('revert', 'Revert')], verbose_name='Тип'),
        ),
        migrations.AddConstraint(
            model_name='article',
            constraint=models.UniqueConstraint(fields=('category', 'name'), name='web_article_unique'),
        ),
        migrations.AddConstraint(
            model_name='articlelogentry',
            constraint=models.UniqueConstraint(fields=('article', 'rev_number'), name='web_articlelogentry_unique'),
        ),
        migrations.AddConstraint(
            model_name='category',
            constraint=models.UniqueConstraint(fields=('name',), name='web_category_unique'),
        ),
        migrations.AddConstraint(
            model_name='externallink',
            constraint=models.UniqueConstraint(fields=('link_from', 'link_to', 'link_type'), name='web_externallink_unique'),
        ),
        migrations.AddConstraint(
            model_name='file',
            constraint=models.UniqueConstraint(fields=('article', 'name', 'deleted_at'), name='web_file_unique'),
        ),
        migrations.AddConstraint(
            model_name='tag',
            constraint=models.UniqueConstraint(fields=('category', 'name'), name='web_tag_unique'),
        ),
        migrations.AddConstraint(
            model_name='tagscategory',
            constraint=models.UniqueConstraint(fields=('slug',), name='web_tagscategory_unique'),
        ),
        migrations.AddConstraint(
            model_name='vote',
            constraint=models.UniqueConstraint(fields=('article', 'user'), name='web_vote_unique'),
        ),
    ]
