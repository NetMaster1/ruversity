# Generated by Django 3.1.3 on 2022-10-11 09:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_content', '0030_auto_20221011_1212'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='additionalmateriallink',
            name='additional_file',
        ),
    ]