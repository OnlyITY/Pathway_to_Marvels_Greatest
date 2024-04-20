# Generated by Django 5.0.2 on 2024-04-20 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0003_remove_users_user_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='characters',
            name='characterDescription',
            field=models.TextField(default='Description'),
        ),
        migrations.AddField(
            model_name='characters',
            name='characterId',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='characters',
            name='characterImage',
            field=models.TextField(default='Image'),
        ),
    ]
