from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from movielens_app.views import UploadView, FileUploadDetailView, HomeView, MovieDetailView

urlpatterns = [
    path("__reload__/", include("django_browser_reload.urls")),
    path('admin/', admin.site.urls, name="admin"),
    path('', HomeView.as_view(), name="index"),
    path('movie/<int:pk>/', MovieDetailView.as_view(), name="movie-detail"),
    path('upload/', UploadView.as_view(), name="upload"),
    path('upload/<int:pk>/', FileUploadDetailView.as_view(), name='upload_detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
