# Generated by Django 3.1.3 on 2022-11-14 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_content', '0051_auto_20221114_1319'),
    ]

    operations = [
        migrations.AddField(
            model_name='library',
            name='length',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='library',
            name='length_1',
            field=models.DurationField(null=True),
        ),
        migrations.AddField(
            model_name='library',
            name='size_mb',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
