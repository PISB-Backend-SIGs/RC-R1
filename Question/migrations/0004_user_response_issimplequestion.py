# Generated by Django 4.1.7 on 2023-03-18 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Question', '0003_easyquestion'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_response',
            name='isSimpleQuestion',
            field=models.BooleanField(default=False),
        ),
    ]
