# Generated by Django 3.1.3 on 2021-04-04 00:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_content', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lecture',
            old_name='course',
            new_name='subject',
        ),
    ]
