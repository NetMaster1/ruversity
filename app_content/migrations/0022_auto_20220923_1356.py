# Generated by Django 3.1.3 on 2022-09-23 10:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app_content', '0021_auto_20220919_1405'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lecture',
            name='author',
            field=models.ForeignKey(default='Ruversity', null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='mainsubject',
            name='author',
            field=models.ForeignKey(default='Ruversity', null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to=settings.AUTH_USER_MODEL),
        ),
    ]
