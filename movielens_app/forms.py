import pandas as pd
import time
from datetime import timedelta
from django import forms
from .models import FileUpload, Movie, Rating, Tag, Link, GenomeScore, GenomeTag

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
                    data_dict['movieId'] = int(data_dict['movieId'])
                if 'tagId' in data_dict:
                    data_dict['tagId'] = int(data_dict['tagId'])
                obj = model(**data_dict)
                obj.save()
                records_inserted += 1
                print(records_inserted)
            except Exception as e:
                records_failed += 1
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
        return records_inserted, records_failed
