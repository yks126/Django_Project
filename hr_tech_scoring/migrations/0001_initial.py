# Generated by Django 4.2.11 on 2024-04-08 03:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='resume_scores_db',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_code', models.CharField(max_length=100)),
                ('row_id', models.CharField(max_length=100)),
                ('score_1', models.IntegerField(default=None, null=True)),
                ('score_2', models.IntegerField(default=None, null=True)),
                ('score_3', models.IntegerField(default=None, null=True)),
                ('score_4', models.IntegerField(default=None, null=True)),
                ('score_5', models.IntegerField(default=None, null=True)),
                ('score_6', models.IntegerField(default=None, null=True)),
                ('marked', models.BooleanField(default=False)),
                ('notes', models.CharField(default='', max_length=100, null=True)),
                ('expand_edu', models.IntegerField(default=0)),
                ('expand_experience', models.IntegerField(default=0)),
                ('expand_intro', models.IntegerField(default=0)),
                ('last_modify_date', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'resume_scores',
            },
        ),
        migrations.CreateModel(
            name='user_char_db',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_code', models.CharField(max_length=100)),
                ('user_password', models.CharField(max_length=100)),
                ('last_modify_date', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'user_char',
            },
        ),
    ]
