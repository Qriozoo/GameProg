# Generated by Django 4.1.2 on 2023-03-25 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_task_level'),
    ]

    operations = [
        migrations.AddField(
            model_name='solution',
            name='likes',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
    ]
