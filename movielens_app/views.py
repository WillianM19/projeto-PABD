from django.shortcuts import render
from django.views.generic import FormView

from movielens_app.forms import UploadForm

class UploadView(FormView):
    template_name = 'upload.html'
    form_class = UploadForm
    success_url = '/upload/'

