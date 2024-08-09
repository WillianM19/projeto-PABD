from django.db import models
from django.utils import timezone

class Rating(models.Model):
    userId = models.IntegerField()
    movieId = models.ForeignKey('Movie', on_delete=models.CASCADE)
    rating = models.FloatField()
    timestamp = models.BigIntegerField()

    def __str__(self):
        return f'Usuário {self.userId} avaliou Filme {self.movieId} com {self.rating}'

class Tag(models.Model):
    userId = models.IntegerField()
    movieId = models.ForeignKey('Movie', on_delete=models.CASCADE)
    tag = models.CharField(max_length=255)
    timestamp = models.BigIntegerField()

    def __str__(self):
        return f'Usuário {self.userId} etiquetou Filme {self.movieId} com {self.tag}'

class Movie(models.Model):
    movieId = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    genres = models.CharField(max_length=255)

    def __str__(self):
        return self.title

class Link(models.Model):
    movieId = models.OneToOneField(Movie, on_delete=models.CASCADE)
    imdbId = models.CharField(max_length=255)
    tmdbId = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.movieId.title} (IMDb: {self.imdbId}, TMDb: {self.tmdbId})'

class GenomeScore(models.Model):
    movieId = models.ForeignKey(Movie, on_delete=models.CASCADE)
    tagId = models.IntegerField()
    relevance = models.FloatField()

    def __str__(self):
        return f'Filme {self.movieId} - Etiqueta {self.tagId}: {self.relevance}'

class GenomeTag(models.Model):
    tagId = models.IntegerField()
    tag = models.CharField(max_length=255)

    def __str__(self):
        return self.tag

from django.db import models

class FileUpload(models.Model):
    file_name = models.CharField(max_length=255)
    file = models.FileField(upload_to='uploads/')
    processing_time = models.DurationField(null=True, blank=True)  # Permitir valores nulos
    records_inserted = models.IntegerField(null=True, blank=True)
    records_failed = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.file_name
    

