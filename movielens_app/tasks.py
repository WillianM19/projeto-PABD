import time
import pandas as pd
from datetime import timedelta
from celery import shared_task
from django.core.files.storage import default_storage
from .models import FileUpload, Movie, Rating, Tag, Link, GenomeScore, GenomeTag

@shared_task
def add(x, y):
    return x + y

@shared_task
def hello_world_task():
    print("Hello, World!")

@shared_task
def process_file_task(file_name, file_upload_id):
    try:
        # Recupera a instância de FileUpload
        file_upload = FileUpload.objects.get(id=file_upload_id)
        file_path = file_upload.file.path
        print(f"Processing file: {file_path}")

        if not file_name.endswith('.csv'):
            raise ValueError("O arquivo deve ser um CSV")

        start_time = time.time()
        data = pd.read_csv(file_path)
        records_inserted = 0
        records_failed = 0

        try:
            if file_name == 'movies.csv':
                records_inserted, records_failed = _process_csv(data, Movie, ['movieId', 'title', 'genres'])
            elif file_name == 'ratings.csv':
                records_inserted, records_failed = _process_csv(data, Rating, ['userId', 'movieId', 'rating', 'timestamp'])
            elif file_name == 'tags.csv':
                records_inserted, records_failed = _process_csv(data, Tag, ['userId', 'movieId', 'tag', 'timestamp'])
            elif file_name == 'links.csv':
                records_inserted, records_failed = _process_links_csv(data)
            elif file_name == 'genome-scores.csv':
                records_inserted, records_failed = _process_csv(data, GenomeScore, ['movieId', 'tagId', 'relevance'])
            elif file_name == 'genome-tags.csv':
                records_inserted, records_failed = _process_csv(data, GenomeTag, ['tagId', 'tag'])
            else:
                raise ValueError("Formato de arquivo não suportado")
        except Exception as e:
            print(f"Erro ao processar o arquivo: {e}")
            records_failed += 1

        end_time = time.time()
        processing_time_seconds = end_time - start_time
        processing_time = timedelta(seconds=processing_time_seconds)

        # Atualiza a instância de FileUpload com os resultados do processamento
        file_upload.processing_time = processing_time
        file_upload.records_inserted = records_inserted
        file_upload.records_failed = records_failed
        file_upload.save()

    except Exception as e:
        print(f"Erro na tarefa Celery: {e}")

    end_time = time.time()
    processing_time_seconds = end_time - start_time
    processing_time = timedelta(seconds=processing_time_seconds)

    # Atualiza a instância de FileUpload com os resultados do processamento
    file_upload.processing_time = processing_time
    file_upload.records_inserted = records_inserted
    file_upload.records_failed = records_failed
    file_upload.save()

def _process_csv(data, model, columns):
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

def _process_links_csv(data):
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
