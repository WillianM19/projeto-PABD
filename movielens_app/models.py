from django.db import models

class Rating(models.Model):
    user_id = models.IntegerField()
    movie_id = models.IntegerField()
    rating = models.FloatField()
    timestamp = models.BigIntegerField()

    def __str__(self):
        return f'Usuário {self.user_id} avaliou Filme {self.movie_id} com {self.rating}'

class Tag(models.Model):
    user_id = models.IntegerField()
    movie_id = models.IntegerField()
    tag = models.CharField(max_length=255)
    timestamp = models.BigIntegerField()

    def __str__(self):
        return f'Usuário {self.user_id} etiquetou Filme {self.movie_id} com {self.tag}'

class Movie(models.Model):
    movie_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    genres = models.CharField(max_length=255)

    def __str__(self):
        return self.title

class Link(models.Model):
    movie_id = models.OneToOneField(Movie, on_delete=models.CASCADE, primary_key=True)
    imdb_id = models.CharField(max_length=255)
    tmdb_id = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.movie_id.title} (IMDb: {self.imdb_id}, TMDb: {self.tmdb_id})'

class GenomeScore(models.Model):
    movie_id = models.IntegerField()
    tag_id = models.IntegerField()
    relevance = models.FloatField()

    def __str__(self):
        return f'Filme {self.movie_id} - Etiqueta {self.tag_id}: {self.relevance}'

class GenomeTag(models.Model):
    tag_id = models.IntegerField(primary_key=True)
    tag = models.CharField(max_length=255)

    def __str__(self):
        return self.tag

class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    upload_time = models.DateTimeField(auto_now_add=True)
    processing_time = models.FloatField(null=True, blank=True)
    successful_records = models.IntegerField(default=0)
    failed_records = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=[('Processing', 'Processing'), ('Completed', 'Completed'), ('Failed', 'Failed')])

