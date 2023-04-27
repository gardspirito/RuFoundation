# Generated by Django 4.0.6 on 2023-04-27 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0010_alter_user_api_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='forum_inactive_until',
            field=models.DateTimeField(null=True, verbose_name='Деактивировать форум до'),
        ),
        migrations.AddField(
            model_name='user',
            name='inactive_until',
            field=models.DateTimeField(null=True, verbose_name='Деактивировать до'),
        ),
        migrations.AddField(
            model_name='user',
            name='is_forum_active',
            field=models.BooleanField(default=True, verbose_name='Активирован форум'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Активирован'),
        ),
    ]
