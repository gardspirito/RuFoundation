# Generated by Django 4.0.6 on 2024-09-22 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0015_visualusergroup_user_visual_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='visualusergroup',
            name='index',
            field=models.IntegerField(default=0, verbose_name='Порядок в списках'),
        ),
    ]