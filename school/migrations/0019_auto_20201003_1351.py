# Generated by Django 3.0.8 on 2020-10-03 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0018_auto_20201001_1913'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='classroom',
            name='RSA',
        ),
        migrations.AddField(
            model_name='classroom',
            name='password',
            field=models.CharField(blank='True', max_length=156),
        ),
    ]
