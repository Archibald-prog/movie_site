from django.urls import path

from . import views

urlpatterns = [
    path('', views.MoviesView.as_view()),  # http://127.0.0.1:8000/
    path("<slug:slug>/", views.MovieDetailView.as_view(), name="movie_detail"),
    path('review/<int:pk>/', views.AddReview.as_view(), name="add_review"),  # http://127.0.0.1:8000/review/2/
    path("actor/<slug:slug>/", views.ActorView.as_view(), name="actor_detail"),
]
