# Generated by Django 4.1.7 on 2023-02-23 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Question', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user_response',
            name='response',
        ),
        migrations.AddField(
            model_name='user_response',
            name='response1',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='user_response',
            name='response2',
            field=models.IntegerField(null=True),
        ),
    ]
