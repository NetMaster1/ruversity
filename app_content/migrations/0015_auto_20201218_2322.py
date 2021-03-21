# Generated by Django 3.1.3 on 2020-12-18 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_content', '0014_auto_20201215_0159'),
    ]

    operations = [
        migrations.AddField(
            model_name='mainsubject',
            name='av_rating',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=3),
        ),
        migrations.AddField(
            model_name='mainsubject',
            name='quantity',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='mainsubject',
            name='total',
            field=models.IntegerField(null=True),
        ),
    ]
