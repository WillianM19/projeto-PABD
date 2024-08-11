from django import forms
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import FormView

from movielens_app.tasks import process_csv_file

from .forms import UploadForm
from movielens_app.models import FileUpload

class UploadView(FormView):
    template_name = 'upload.html'
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
    template_name = 'upload_detail.html'
    context_object_name = 'upload'