# Generated by Django 5.0.7 on 2024-08-15 08:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_verse', '0008_alter_post_blog'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blog',
            old_name='created',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='blog',
            old_name='updated',
            new_name='updated_at',
        ),
    ]
