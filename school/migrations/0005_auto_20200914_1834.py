# Generated by Django 3.0.8 on 2020-09-14 10:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0004_announcement_comments'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='comments',
            new_name='comment',
        ),
    ]
