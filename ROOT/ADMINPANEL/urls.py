from django.contrib.auth import views as logview
from django.urls import path
from . import views

app_name = "ADMINPANEL"


urlpatterns = [
# university/adminpanel/
    path("", views.admin_home, name='admin_home'),
    path("uploadfiles/", views.upload_files, name='uploadfiles'),
    path("upload_data/<int:dataBaseKey>", views.upload_data, name='upload_data'),
    path("download_data/", views.download_data, name='download_data'),
]
