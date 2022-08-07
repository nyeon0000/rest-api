from django.urls import path
from .views import *
from . import views

app_name="myapp"
urlpatterns=[
    path('', views.movie_list_create),
    path('<int:movie_pk>/', views.movie_detail_update_delete),
]