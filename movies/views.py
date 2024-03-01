from django.views.generic import ListView, DetailView

from .models import Movie


class MoviesView(ListView):
    """Список фильмов"""
    model = Movie
    queryset = Movie.objects.filter(draft=False)


class MovieDetailView(DetailView):
    """Вывод информации о фильме"""
    model = Movie
