from celery import shared_task
import pandas as pd
from .models import FileUpload, Movie, Rating, Tag, Link, GenomeScore, GenomeTag
import time
from datetime import timedelta
from django.utils import timezone
from django.core.files.storage import default_storage
import logging
logger = logging.getLogger(__name__)

@shared_task
def process_csv_file(file_path, file_name):
    logger.info(f"Iniciando processamento do arquivo: {file_name}")
    start_time = time.time()
    
    records_inserted = 0
    records_failed = 0

    try:
        with default_storage.open(file_path) as file:
            data = pd.read_csv(file)

        if file_name == 'movies.csv':
            records_inserted, records_failed = _process_csv_bulk(data, Movie, ['movieId', 'title', 'genres'])
        elif file_name == 'ratings.csv':
            records_inserted, records_failed = _process_csv_bulk(data, Rating, ['userId', 'movieId', 'rating', 'timestamp'])
        elif file_name == 'tags.csv':
            records_inserted, records_failed = _process_csv_bulk(data, Tag, ['userId', 'movieId', 'tag', 'timestamp'])
        elif file_name == 'links.csv':
            records_inserted, records_failed = _process_links_csv_bulk(data)
        elif file_name == 'genome-scores.csv':
            records_inserted, records_failed = _process_csv_bulk(data, GenomeScore, ['movieId', 'tagId', 'relevance'])
        elif file_name == 'genome-tags.csv':
            records_inserted, records_failed = _process_csv_bulk(data, GenomeTag, ['tagId', 'tag'])
        else:
            raise Exception("Formato de arquivo não suportado")

    except Exception as e:
        logger.error(f"Erro ao processar o arquivo: {e}")
        records_failed += 1

    end_time = time.time()
    processing_time_seconds = end_time - start_time
    processing_time = timedelta(seconds=processing_time_seconds)

    file_upload = FileUpload.objects.create(
        file_name=file_name,
        upload_date=timezone.now(),
        processing_time=processing_time,
        records_inserted=records_inserted,
        records_failed=records_failed
    )

    logger.info(f"Arquivo {file_name} processado com sucesso.")
    return file_upload.id

def _process_csv_bulk(data, model, columns):
    records_inserted = 0
    records_failed = 0
    bulk_create_list = []

    for _, row in data.iterrows():
        try:
            data_dict = {col: row[col] for col in columns}
            if 'movieId' in data_dict:
                data_dict['movieId'] = int(data_dict['movieId'])
            if 'tagId' in data_dict:
                data_dict['tagId'] = int(data_dict['tagId'])
            bulk_create_list.append(model(**data_dict))
            records_inserted += 1
        except Exception as e:
            records_failed += 1
            print(f"Erro ao processar linha: {e}")

    if bulk_create_list:
        model.objects.bulk_create(bulk_create_list, batch_size=1000)
    
    return records_inserted, records_failed

def _process_links_csv_bulk(data):
    records_inserted = 0
    records_failed = 0
    bulk_create_list = []

    for _, row in data.iterrows():
        try:
            movie_id = int(row['movieId'])
            movie_instance = Movie.objects.get(movieId=movie_id)
            bulk_create_list.append(Link(
                movieId=movie_instance,
                imdbId=row['imdbId'],
                tmdbId=row['tmdbId']
            ))
            records_inserted += 1
        except Exception as e:
            records_failed += 1
            print(f"Erro ao processar linha: {e}")

    if bulk_create_list:
        Link.objects.bulk_create(bulk_create_list, batch_size=1000)
    
    return records_inserted, records_failed
