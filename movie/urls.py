from django.urls import path
from authentication.views import *
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('movieslist/',views.movielist,name="movies-list"),
    path('movie/<int:mid>/',views.moviedetails,name="movie-details"),
]