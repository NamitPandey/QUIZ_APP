from django.contrib.auth import views as logview
from django.urls import path
from . import views

app_name = "ADMINPANEL"


urlpatterns = [
# university/adminpanel/
    path("", views.admin_home, name='admin_home'),
    path("upload_data/<int:dataBaseKey>", views.upload_data, name='upload_data'),
]
