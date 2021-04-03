# Generated by Django 3.1.3 on 2021-04-03 15:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Badword',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('badword', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Credit_card_type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='DiscountOn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discount_on', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='MainSubject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(null=True)),
                ('prerequisite', models.TextField(null=True)),
                ('date_posted', models.DateField(auto_now_add=True)),
                ('thumbnail_file', models.FileField(upload_to='uploads')),
                ('percent', models.CharField(default='0%', max_length=50)),
                ('total', models.IntegerField(default=0)),
                ('quantity', models.IntegerField(default=0)),
                ('av_rating', models.DecimalField(decimal_places=1, default=0, max_digits=3)),
                ('transactions', models.IntegerField(default=0)),
                ('ready', models.BooleanField(default=False)),
                ('checked', models.BooleanField(default=False)),
                ('blocked', models.BooleanField(default=False)),
                ('discount_programs', models.BooleanField(default=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app_content.category')),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app_content.language')),
            ],
        ),
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('regular', models.DecimalField(decimal_places=2, max_digits=5)),
                ('discount', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
        migrations.CreateModel(
            name='TempImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('temp_thumbnail_file', models.FileField(upload_to='uploads')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_bought', models.DateField(auto_now_add=True)),
                ('paid_amount', models.FloatField(null=True)),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_content.mainsubject')),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField()),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_content.mainsubject')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Paypal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='mainsubject',
            name='price',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app_content.price'),
        ),
        migrations.CreateModel(
            name='Main_method',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('method', models.CharField(max_length=50)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Lecture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('date_posted', models.DateTimeField(auto_now_add=True)),
                ('video_file', models.FileField(null=True, upload_to='uploads')),
                ('blocked', models.BooleanField(default=False)),
                ('free', models.BooleanField(default=False)),
                ('length', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('size_mb', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('chapter', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app_content.chapter')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app_content.mainsubject')),
            ],
        ),
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keyword', models.CharField(max_length=50)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Credit_card',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_number', models.CharField(max_length=50)),
                ('card_type', models.CharField(max_length=50, null=True)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='chapter',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app_content.mainsubject'),
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateField(auto_now_add=True)),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_content.mainsubject')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Bank_account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=50)),
                ('entity_name', models.CharField(blank=True, max_length=50)),
                ('itin', models.CharField(blank=True, max_length=50)),
                ('bin', models.CharField(blank=True, max_length=50)),
                ('bank_account', models.CharField(blank=True, max_length=50)),
                ('account', models.CharField(max_length=50)),
                ('ready', models.BooleanField(default=False)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
