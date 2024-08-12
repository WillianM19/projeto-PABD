from django.contrib import admin
from .models import FileUpload, Rating, Tag, Movie, Link, GenomeScore, GenomeTag

admin.site.register(Rating)
admin.site.register(Tag)
admin.site.register(Movie)
admin.site.register(Link)
admin.site.register(GenomeScore)
admin.site.register(GenomeTag)
admin.site.register(FileUpload)