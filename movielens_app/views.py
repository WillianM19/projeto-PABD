import requests
from django import forms
from django.shortcuts import redirect
from django.db.models import Avg
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.views.generic import DetailView, ListView
from django.views.generic.edit import FormView

from .forms import UploadForm
from .models import Movie, Rating
from .tasks import hello_world_task
from movielens_app.models import FileUpload

def teste(request):
    hello_world_task.delay()
    return redirect('upload')

class HomeView(ListView):
    template_name = 'index.html'
    model = Movie
    paginate_by = 15

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginated_movies = context['page_obj'].object_list

        movie_ratings = (
            Rating.objects.filter(movieId__in=paginated_movies)
            .values('movieId')
            .annotate(average_rating=Avg('rating'))
        )

        return context
    
class MovieDetailView(DetailView):
    model = Movie
    template_name = 'movies/movie-detail.html'
    context_object_name = 'movie'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        movie = context['movie']
        
        # Fetch details from OMDb API
        omdb_api_key = 'YOUR_OMDB_API_KEY'
        omdb_url = f'http://www.omdbapi.com/?i={movie.link.imdbId}&apikey={omdb_api_key}'
        omdb_response = requests.get(omdb_url)
        context['omdb_data'] = omdb_response.json()

        # Fetch details from TMDb API
        tmdb_api_key = 'YOUR_TMDB_API_KEY'
        tmdb_url = f'https://api.themoviedb.org/3/movie/{movie.link.tmdbId}?api_key={tmdb_api_key}'
        tmdb_response = requests.get(tmdb_url)
        context['tmdb_data'] = tmdb_response.json()
        
        return context
    

class UploadView(FormView):
    template_name = 'uploads/upload.html'
    form_class = UploadForm
    success_url = reverse_lazy('upload') 

    def form_valid(self, form):
        try:
            file_uploaded = form.process_file() 
            return redirect(f'/upload/{file_uploaded.id}/')
        except forms.ValidationError as e:
            form.add_error(None, e)  
            return self.form_invalid(form)

class FileUploadDetailView(DetailView):
    model = FileUpload
    template_name = 'uploads/upload_detail.html'
    context_object_name = 'upload'