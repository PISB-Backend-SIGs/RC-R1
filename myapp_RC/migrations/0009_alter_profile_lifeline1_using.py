# Generated by Django 4.1.1 on 2023-04-16 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp_RC', '0008_profile_lifeline1_using'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='lifeline1_using',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
