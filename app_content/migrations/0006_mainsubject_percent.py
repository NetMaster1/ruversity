# Generated by Django 3.1.3 on 2020-12-10 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_content', '0005_auto_20201205_2345'),
    ]

    operations = [
        migrations.AddField(
            model_name='mainsubject',
            name='percent',
            field=models.CharField(default='50%', max_length=50),
        ),
    ]