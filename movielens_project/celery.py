from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Define o ambiente padrão do Django para o Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movielens_project.settings')

app = Celery('movielens_project')

# Usa uma string aqui para que o worker não precise serializar
# o objeto configuração para o processo filho.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Carrega as tarefas dos módulos de Django app
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
