from django.urls import path
from .views import *
from . import views

app_name="myapp"
urlpatterns=[
    path('', views.movie_list_create),
    path('<int:movie_pk>/', views.movie_detail_update_delete),
    path('<int:movie_pk>/reviews/', views.review_list_create),
    path('<int:movie_pk>/reviews/<int:review_pk>', views.review_detail_update_delete),
    path('regist/', user_regist, name = 'regist'),
    path('login/', user_login, name = 'login'),
    path('test/', test, name = 'test'),
]