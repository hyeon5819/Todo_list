# Generated by Django 4.2 on 2023-04-27 18:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0002_alter_todo_content'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='todo',
            name='content',
        ),
    ]
