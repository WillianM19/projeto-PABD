from django.contrib import admin
from .models import Rating, Tag, Movie, Link, GenomeScore, GenomeTag, FileUpload

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['userId', 'movieId', 'rating', 'timestamp']
    search_fields = ['userId', 'movieId__title']
    list_per_page = 15  

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['userId', 'movieId', 'tag', 'timestamp']
    search_fields = ['userId', 'movieId__title', 'tag']
    list_per_page = 15  

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['movieId', 'title', 'genres']
    search_fields = ['title', 'genres']
    list_per_page = 15  

@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ['movieId', 'imdbId', 'tmdbId']
    search_fields = ['movieId__title', 'imdbId', 'tmdbId']
    list_per_page = 15  

@admin.register(GenomeScore)
class GenomeScoreAdmin(admin.ModelAdmin):
    list_display = ['movieId', 'tagId', 'relevance']
    search_fields = ['movieId__title', 'tagId']
    list_per_page = 15  

@admin.register(GenomeTag)
class GenomeTagAdmin(admin.ModelAdmin):
    list_display = ['tagId', 'tag']
    search_fields = ['tagId', 'tag']
    list_per_page = 15  

@admin.register(FileUpload)
class FileUploadAdmin(admin.ModelAdmin):
    list_display = ('file_name', 'processing_time', 'records_inserted', 'records_failed')
