from django.contrib import admin
from .models import Rating, Tag, Movie, Link, GenomeScore, GenomeTag

admin.site.register(Rating)
admin.site.register(Tag)
admin.site.register(Movie)
admin.site.register(Link)
admin.site.register(GenomeScore)
admin.site.register(GenomeTag)