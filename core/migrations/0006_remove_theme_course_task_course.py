# Generated by Django 4.1.7 on 2023-03-21 09:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_course_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='theme',
            name='course',
        ),
        migrations.AddField(
            model_name='task',
            name='course',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='core.course'),
            preserve_default=False,
        ),
    ]
