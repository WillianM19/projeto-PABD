# Generated by Django 5.0.7 on 2024-08-07 02:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movielens_app', '0002_fileupload_delete_uploadedfile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='id',
        ),
        migrations.AlterField(
            model_name='movie',
            name='movieId',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
