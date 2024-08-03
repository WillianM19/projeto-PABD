from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from movielens_app.views import UploadView

urlpatterns = [
    path('admin/', admin.site.urls, name="admin"),
    path('upload/', UploadView.as_view(), name="upload")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
