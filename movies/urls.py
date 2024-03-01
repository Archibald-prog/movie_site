from django.urls import path

from . import views

urlpatterns = [
    path('', views.MoviesView.as_view()),  # http://127.0.0.1:8000/
    path("<slug:slug>/", views.MovieDetailView.as_view(), name="movie_detail")  # http://127.0.0.1:8000/some-slug/
]
