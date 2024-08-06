from django import forms
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import FormView

from .forms import UploadForm
from movielens_app.models import FileUpload

class UploadView(FormView):
    template_name = 'upload.html'
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
    template_name = 'upload_detail.html'
    context_object_name = 'upload'