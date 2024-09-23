# Generated by Django 5.1.1 on 2024-09-23 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='client_id',
            field=models.CharField(default='', max_length=256),
        ),
        migrations.AddField(
            model_name='user',
            name='selected_repo_id',
            field=models.BigIntegerField(default=0),
        ),
    ]
