# myproject/__init__.py

from __future__ import absolute_import, unicode_literals

# Este módulo é necessário para que o Celery carregue automaticamente as tarefas registradas
from .celery import app as celery_app

__all__ = ('celery_app',)
