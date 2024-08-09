from django import forms
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .models import FileUpload
from .tasks import process_file_task, hello_world_task, add

class UploadForm(forms.Form):
    file = forms.FileField()

    def process_file(self):
        file = self.files['file']
        if not file.name.endswith('.csv'):
            raise forms.ValidationError("O arquivo deve ser um CSV")

        add.delay(4, 4)

        hello_world_task.delay()

        # Salvar o arquivo no armazenamento temporário
        file_path = default_storage.save(f'uploads/{file.name}', ContentFile(file.read()))

        # Criar uma instância de FileUpload
        file_upload = FileUpload.objects.create(
            file_name=file.name,
            file=file_path
        )

        # Dispara a tarefa assíncrona
        process_file_task.delay(file.name, file_upload.id)

        return file_upload
