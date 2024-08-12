from django.contrib import admin
from .models import Rating, Tag, Movie, Link, GenomeScore, GenomeTag, FileUpload

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('userId', 'movieId', 'rating', 'timestamp')
    search_fields = ('userId', 'movieId')
    ordering = ('userId',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('userId', 'movieId', 'tag', 'timestamp')
    search_fields = ('userId', 'movieId', 'tag')
    ordering = ('userId',)
    

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('movieId', 'title', 'genres')
    search_fields = ('title', 'genres')
    ordering = ('movieId',)

@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ('movieId', 'imdbId', 'tmdbId')
    search_fields = ('imdbId', 'tmdbId')
    ordering = ('movieId',)
    readonly_fields = ('movieId',)
    
@admin.register(GenomeScore)
class GenomeScoreAdmin(admin.ModelAdmin):
    list_display = ('movieId', 'tagId', 'relevance')
    search_fields = ('movieId', 'tagId')
    list_filter = ('relevance',)
    ordering = ('movieId', 'tagId')

@admin.register(GenomeTag)
class GenomeTagAdmin(admin.ModelAdmin):
    list_display = ('tagId', 'tag')
    search_fields = ('tagId', 'tag')
    ordering = ('tagId',)

@admin.register(FileUpload)
class FileUploadAdmin(admin.ModelAdmin):
    list_display = ('file_name', 'upload_date', 'processing_time', 'records_inserted', 'records_failed', 'task_id')
    search_fields = ('file_name', 'task_id')
    list_filter = ('upload_date',)
    ordering = ('-upload_date',)
