# Generated by Django 3.0.8 on 2020-09-13 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='following',
        ),
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.CharField(default=1, max_length=7),
            preserve_default=False,
        ),
    ]