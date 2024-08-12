import time
import pandas as pd
from datetime import timedelta
from django import forms
from .models import FileUpload, Movie, Rating, Tag, Link, GenomeScore, GenomeTag
from django.db import connection
import tempfile
import os

class UploadForm(forms.Form):
    file = forms.FileField()

    def process_file(self):
        file = self.files['file']
        if not file.name.endswith('.csv'):
            raise forms.ValidationError("O arquivo deve ser um CSV")

        start_time = time.time()
        data = pd.read_csv(file)
        file_name = file.name
        records_inserted = 0
        records_failed = 0

        try:
            if file_name == 'movies.csv':
                records_inserted, records_failed = self._process_csv(data, Movie, ['movieId', 'title', 'genres'])
            elif file_name == 'ratings.csv':
                records_inserted, records_failed = self._process_csv(data, Rating, ['userId', 'movieId', 'rating', 'timestamp'])
            elif file_name == 'tags.csv':
                records_inserted, records_failed = self._process_csv(data, Tag, ['userId', 'movieId', 'tag', 'timestamp'])
            elif file_name == 'links.csv':
                records_inserted, records_failed = self._process_links_csv(data)
            elif file_name == 'genome-scores.csv':
                records_inserted, records_failed = self._process_csv(data, GenomeScore, ['movieId', 'tagId', 'relevance'])
            elif file_name == 'genome-tags.csv':
                records_inserted, records_failed = self._process_csv(data, GenomeTag, ['tagId', 'tag'])
            else:
                raise forms.ValidationError("Formato de arquivo não suportado")
        except Exception as e:
            records_failed += 1

        end_time = time.time()
        processing_time_seconds = end_time - start_time
        processing_time = timedelta(seconds=processing_time_seconds)

        file_upload = FileUpload.objects.create(
            file_name=file_name,
            processing_time=processing_time,
            records_inserted=records_inserted,
            records_failed=records_failed
        )
        
        return file_upload

    def _process_csv(self, data, model, columns):
        # Processar e salvar os dados no banco de dados
        records_inserted = 0
        records_failed = 0
        
        for _, row in data.iterrows():
            try:
                data_dict = {col: row[col] for col in columns}
                if 'movieId' in data_dict:
                    movie_id = int(data_dict['movieId'])
                    if model == Rating or model == Tag:  # Somente para Rating e Tag
                        data_dict['movieId'] = Movie.objects.get(movieId=movie_id)  # Obtém a instância de Movie
                    else:
                        data_dict['movieId'] = movie_id
                if 'tagId' in data_dict:
                    data_dict['tagId'] = int(data_dict['tagId'])
                if 'tag' in data_dict:
                    data_dict['tag'] = str(data_dict['tag'])
                if 'userId' in data_dict:
                    data_dict['userId'] = int(data_dict['userId'])
                if 'rating' in data_dict:
                    data_dict['rating'] = float(data_dict['rating'])
                if 'timestamp' in data_dict:
                    data_dict['timestamp'] = int(data_dict['timestamp'])
                obj = model(**data_dict)
                obj.save()
                records_inserted += 1
            except Exception as e:
                records_failed += 1
                print(f"Failed to process row {row}: {e}")
        return records_inserted, records_failed
    
    def _process_links_csv(self, data):
        records_inserted = 0
        records_failed = 0
        for _, row in data.iterrows():
            try:
                movie_id = int(row['movieId'])
                movie_instance = Movie.objects.get(movieId=movie_id)
                link = Link(
                    movieId=movie_instance,
                    imdbId=row['imdbId'],
                    tmdbId=row['tmdbId']
                )
                link.save()
                records_inserted += 1
            except Exception as e:
                records_failed += 1
                print(e)
        return records_inserted, records_failed


class MovieFilterForm(forms.Form):
    genres = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Gêneros (separados por vírgula)',
            'class': 'form-input mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50'
        })
    )
    start_date = forms.DateField(
        required=False,
        widget=forms.TextInput(attrs={
            'type': 'date',
            'class': 'form-input mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50'
        })
    )
    end_date = forms.DateField(
        required=False,
        widget=forms.TextInput(attrs={
            'type': 'date',
            'class': 'form-input mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50'
        })
    )
    min_rating = forms.FloatField(
        required=False,
        min_value=0.5,
        max_value=5.0,
        widget=forms.NumberInput(attrs={
            'step': '0.5',
            'class': 'form-input mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50'
        })
    )
    min_votes = forms.IntegerField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-input mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50'
        })
    )
    user_id = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-input mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50'
        })
    )