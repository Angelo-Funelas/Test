# Generated by Django 3.0.8 on 2020-09-26 01:54

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0009_poll_pollvalues'),
    ]

    operations = [
        migrations.AddField(
            model_name='poll',
            name='choice1value',
            field=models.ManyToManyField(blank='True', related_name='vote1', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='poll',
            name='choice2value',
            field=models.ManyToManyField(blank='True', related_name='vote2', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='poll',
            name='choice3value',
            field=models.ManyToManyField(blank='True', related_name='vote3', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='poll',
            name='choice4value',
            field=models.ManyToManyField(blank='True', related_name='vote4', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='poll',
            name='choice5value',
            field=models.ManyToManyField(blank='True', related_name='vote5', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='poll',
            name='choice6value',
            field=models.ManyToManyField(blank='True', related_name='vote6', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='pollvalues',
        ),
    ]
