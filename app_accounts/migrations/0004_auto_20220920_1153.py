# Generated by Django 3.1.3 on 2022-09-20 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_accounts', '0003_auto_20220512_1957'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='background',
            field=models.TextField(null=True),
        ),
    ]
