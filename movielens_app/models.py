from django.db import models
from django.utils import timezone

class Rating(models.Model):
    userId = models.IntegerField()
    movieId = models.IntegerField()
    rating = models.FloatField()
    timestamp = models.BigIntegerField()

    def __str__(self):
        return f'Usuário {self.userId} avaliou Filme {self.movieId} com {self.rating}'

class Tag(models.Model):
    userId = models.IntegerField()
    movieId = models.IntegerField()
    tag = models.CharField(max_length=255)
    timestamp = models.BigIntegerField()

    def __str__(self):
        return f'Usuário {self.userId} etiquetou Filme {self.movieId} com {self.tag}'

class Movie(models.Model):
    movieId = models.IntegerField()
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
    movieId = models.IntegerField()
    tagId = models.IntegerField()
    relevance = models.FloatField()

    def __str__(self):
        return f'Filme {self.movieId} - Etiqueta {self.tagId}: {self.relevance}'

class GenomeTag(models.Model):
    tagId = models.IntegerField()
    tag = models.CharField(max_length=255)

    def __str__(self):
        return self.tag

class FileUpload(models.Model):
    file_name = models.CharField(max_length=255)
    upload_date = models.DateTimeField(default=timezone.now)
    processing_time = models.DurationField(null=True, blank=True)
    records_inserted = models.IntegerField(default=0)
    records_failed = models.IntegerField(default=0)
    task_id = models.CharField(max_length=255, null=True, blank=True)  # Novo campo

    def __str__(self):
        return self.file_name

    

