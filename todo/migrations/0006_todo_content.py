# Generated by Django 4.2 on 2023-04-28 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0005_alter_todo_completion_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='todo',
            name='content',
            field=models.TextField(blank=True, null=True),
        ),
    ]
