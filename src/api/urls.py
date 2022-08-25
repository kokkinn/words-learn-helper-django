from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('get_pairs', views.getData, name="get_pairs"),
]