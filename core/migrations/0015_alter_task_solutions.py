# Generated by Django 4.1.7 on 2023-04-03 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_remove_solution_task_task_solutions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='solutions',
            field=models.ManyToManyField(blank=True, to='core.solution'),
        ),
    ]