# forms.py

from django import forms
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from movielens_app.models import FileUpload
from .tasks import process_csv_file

class UploadForm(forms.Form):
    file = forms.FileField()

    def process_file(self):
        file = self.files['file']
        if not file.name.endswith('.csv'):
            raise forms.ValidationError("O arquivo deve ser um CSV")

        file_name = file.name
        file_path = default_storage.save(file.name, ContentFile(file.read())) 
        return file_path, file_name

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

