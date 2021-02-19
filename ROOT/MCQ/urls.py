from django.urls import path
from . import views

app_name = "MCQ"

urlpatterns = [
    path("", views.homepage, name='homepage'), # homePage
]
