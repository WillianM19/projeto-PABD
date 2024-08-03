# Generated by Django 5.0.7 on 2024-08-03 20:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GenomeScore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movie_id', models.IntegerField()),
                ('tag_id', models.IntegerField()),
                ('relevance', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='GenomeTag',
            fields=[
                ('tag_id', models.IntegerField(primary_key=True, serialize=False)),
                ('tag', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('movie_id', models.IntegerField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('genres', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('movie_id', models.IntegerField()),
                ('rating', models.FloatField()),
                ('timestamp', models.BigIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('movie_id', models.IntegerField()),
                ('tag', models.CharField(max_length=255)),
                ('timestamp', models.BigIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='UploadedFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='uploads/')),
                ('upload_time', models.DateTimeField(auto_now_add=True)),
                ('processing_time', models.FloatField(blank=True, null=True)),
                ('successful_records', models.IntegerField(default=0)),
                ('failed_records', models.IntegerField(default=0)),
                ('status', models.CharField(choices=[('Processing', 'Processing'), ('Completed', 'Completed'), ('Failed', 'Failed')], max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('movie_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='movielens_app.movie')),
                ('imdb_id', models.CharField(max_length=255)),
                ('tmdb_id', models.CharField(max_length=255)),
            ],
        ),
    ]
