# Generated by Django 3.1.3 on 2022-10-30 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_content', '0039_auto_20221030_1241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lecture',
            name='length_2',
            field=models.DurationField(null=True),
        ),
    ]
