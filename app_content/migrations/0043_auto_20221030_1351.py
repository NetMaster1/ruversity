# Generated by Django 3.1.3 on 2022-10-30 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_content', '0042_auto_20221030_1329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lecture',
            name='length',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='mainsubject',
            name='length',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='section',
            name='length',
            field=models.IntegerField(default=0),
        ),
    ]
