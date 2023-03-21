# Generated by Django 4.1.7 on 2023-03-21 10:26

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='solution',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='solution',
            name='task',
            field=models.ManyToManyField(to='core.task'),
        ),
    ]
