# Generated by Django 3.1.3 on 2021-01-08 11:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_content', '0032_lecture_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lecture',
            name='number',
        ),
    ]
