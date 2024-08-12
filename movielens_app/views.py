import requests
from django import forms
from django.shortcuts import redirect
from django.db.models import Avg, Count
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import FormView

from movielens_app.tasks import process_csv_file

from .models import Movie, Rating
from .forms import UploadForm, MovieFilterForm
from movielens_app.models import FileUpload

class UploadView(FormView):
    template_name = 'uploads/upload.html'
    form_class = UploadForm
    success_url = reverse_lazy('upload') 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['uploads'] = FileUpload.objects.all().order_by('-upload_date')
        return context

    def form_valid(self, form):
        file_path, file_name = form.process_file() 

        process_csv_file.delay(file_path, file_name)

        return redirect(self.success_url)

class FileUploadDetailView(DetailView):
    model = FileUpload
    template_name = 'uploads/upload_detail.html'
    context_object_name = 'upload'

class HomeView(ListView):
    template_name = 'index.html'
    model = Movie
    paginate_by = 15

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginated_movies = context['page_obj'].object_list
        context["search_form"] = MovieFilterForm
        movie_ratings = (
            Rating.objects.filter(movieId__in=paginated_movies)
            .values('movieId')
            .annotate(average_rating=Avg('rating'))
        )

        return context
    
class MovieSearchView(ListView):
    model = Movie
    template_name = 'movies/movie_search.html'
    context_object_name = 'movies'
    paginate_by = 15

    def get_queryset(self):
        form = MovieFilterForm(self.request.GET)
        queryset = Movie.objects.all()

        if form.is_valid():
            genres = form.cleaned_data.get('genres')
            start_date = form.cleaned_data.get('start_date')
            end_date = form.cleaned_data.get('end_date')
            min_rating = form.cleaned_data.get('min_rating')
            min_votes = form.cleaned_data.get('min_votes')
            user_id = form.cleaned_data.get('user_id')

            if genres:
                genres_list = [genre.strip() for genre in genres.split(',')]
                # Cria uma expressão de busca que verifica se qualquer gênero está presente
                genre_query = '|'.join(genres_list)
                queryset = queryset.filter(genres__icontains=genre_query)

            if start_date:
                queryset = queryset.filter(timestamp__gte=start_date)

            if end_date:
                queryset = queryset.filter(timestamp__lte=end_date)

            if min_rating is not None:
                ratings = Rating.objects.values('movieId').annotate(avg_rating=Avg('rating')).filter(avg_rating__gte=min_rating)
                queryset = queryset.filter(id__in=[rating['movieId'] for rating in ratings])

            if min_votes is not None:
                ratings = Rating.objects.values('movieId').annotate(vote_count=Count('rating')).filter(vote_count__gte=min_votes)
                queryset = queryset.filter(id__in=[rating['movieId'] for rating in ratings])

            if user_id is not None:
                queryset = queryset.filter(rating__userId=user_id)

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = MovieFilterForm(self.request.GET)
        context['form'] = form
        return context

class MovieDetailView(DetailView):
    model = Movie
    template_name = 'movies/movie-detail.html'
    context_object_name = 'movie'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        movie = context['movie']
        
        print(movie)
        print(dir(movie.link.imdbId))
        print(movie.link.imdbId.replace('.0', ''))
        print(type(movie.link.imdbId))
        print(int(movie.link.imdbId.replace('.0', '')))

        # Fetch details from OMDb API
        omdb_api_key = '3e3f6376'
        movie_imdb = movie.link.imdbId
        omdb_url = f'http://www.omdbapi.com/?i={movie_imdb}&apikey={omdb_api_key}'
        omdb_response = requests.get(omdb_url)
        context['omdb_data'] = omdb_response.json()

        # Fetch details from TMDb API
        tmdb_api_key = '2fc487799292af1ddbd79c47ba143ed4'
        tmdb_url = f'https://api.themoviedb.org/3/movie/{movie.link.tmdbId}?api_key={tmdb_api_key}'
        tmdb_response = requests.get(tmdb_url)
        context['tmdb_data'] = tmdb_response.json()
        
        return context