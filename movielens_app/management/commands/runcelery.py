from django.core.management.base import BaseCommand
import subprocess

class Command(BaseCommand):
    def handle(self, *args, **options):
        # Define o comando a ser executado
        command = [
            'celery',
            '-A', 'movielens_project',
            'worker',
            '--loglevel=info',
            '-P', 'eventlet'
        ]
        # Executa o comando
        subprocess.call(command)