# Generated by Django 4.1.7 on 2023-02-23 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp_RC', '0004_alter_profile_curr_question'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='answerResponses',
            field=models.TextField(default='[-1]'),
        ),
        migrations.AddField(
            model_name='profile',
            name='questionList',
            field=models.TextField(default='[-1]'),
        ),
    ]
