# Generated by Django 3.1.3 on 2022-11-24 00:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_content', '0053_auto_20221114_1639'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quizquestion',
            name='quiz',
        ),
        migrations.AddField(
            model_name='quizquestion',
            name='lecture',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app_content.lecture'),
        ),
        migrations.DeleteModel(
            name='Quiz',
        ),
    ]
