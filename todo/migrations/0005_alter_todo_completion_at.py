# Generated by Django 4.2 on 2023-04-28 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0004_alter_todo_completion_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='completion_at',
            field=models.DateTimeField(null=True),
        ),
    ]
