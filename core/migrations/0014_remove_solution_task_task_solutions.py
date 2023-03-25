# Generated by Django 4.1.2 on 2023-03-25 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_alter_solution_likes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='solution',
            name='task',
        ),
        migrations.AddField(
            model_name='task',
            name='solutions',
            field=models.ManyToManyField(to='core.solution'),
        ),
    ]
