# Generated by Django 5.0.7 on 2024-08-06 18:28

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movielens_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileUpload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.CharField(max_length=255)),
                ('upload_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('processing_time', models.DurationField()),
                ('records_inserted', models.IntegerField()),
                ('records_failed', models.IntegerField()),
            ],
        ),
        migrations.DeleteModel(
            name='UploadedFile',
        ),
    ]