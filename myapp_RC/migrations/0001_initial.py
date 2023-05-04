# Generated by Django 4.0.5 on 2023-05-04 12:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='chatGPTLifeLine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=1000)),
                ('numUsed', models.IntegerField(default=0)),
                ('lastUsed', models.FloatField(default=100)),
                ('isDepleted', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='EasyQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('easyquestion_no', models.IntegerField()),
                ('easyquestion', models.CharField(max_length=1000)),
                ('easyanswer', models.IntegerField(default=-1)),
                ('question_id', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('user_rank', models.IntegerField(default=1, null=True)),
                ('curr_question', models.IntegerField(default=1)),
                ('questionIndexList', models.TextField(default='[-1]')),
                ('quesno', models.IntegerField(default=1)),
                ('mob_no', models.CharField(max_length=12)),
                ('marks', models.IntegerField(default=0)),
                ('isFirstTry', models.BooleanField(default=True)),
                ('isTimeOut', models.BooleanField(default=False)),
                ('startTime', models.DateTimeField(null=True)),
                ('tempTime', models.DateTimeField(null=True)),
                ('simpleQuestionUsed', models.BooleanField(null=True)),
                ('timeLLUsed', models.BooleanField(default=False)),
                ('remainingTime', models.IntegerField(default=1800)),
                ('lifeline1_count', models.IntegerField(default=0)),
                ('lifeline1_status', models.BooleanField(default=False)),
                ('lifeline1_using', models.BooleanField(null=True)),
                ('lifeline2_status', models.BooleanField(default=False)),
                ('lifeline2_checked', models.BooleanField(default=False)),
                ('focuscount', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_no', models.IntegerField()),
                ('question', models.CharField(max_length=1000)),
                ('answer', models.IntegerField(default=-1)),
            ],
        ),
        migrations.CreateModel(
            name='User_Response',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quetionID', models.IntegerField(default=-1)),
                ('response1', models.CharField(max_length=1000, null=True)),
                ('response2', models.CharField(max_length=1000, null=True)),
                ('isSimpleQuestion', models.BooleanField(default=False)),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('user_profile', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp_RC.profile')),
            ],
        ),
    ]
