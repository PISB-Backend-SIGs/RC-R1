# Generated by Django 4.0.5 on 2023-05-10 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp_RC', '0019_profile_accuracy'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='cache',
            field=models.IntegerField(default=0),
        ),
    ]