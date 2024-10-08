# Generated by Django 5.0.7 on 2024-08-15 16:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0007_telegramchatinfo_created_at_and_more'),
        ('user_verse', '0009_rename_created_blog_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='chat',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='bot.telegramchatinfo'),
        ),
    ]
