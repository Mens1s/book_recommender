from django.urls import path
from . import views

urlpatterns = [
    path('get_books/', views.get_books, name='get_books'),
    path('get_book_info/<str:book_name>/', views.get_book_info, name='get_books'),
    path("popular.html", views.popular, name = "popular"),
    path("recommend.html", views.recommend, name = "recommend"),
    path("index.html", views.main, name = "main"),
    path("", views.main, name = "main"),
    path('api/recommend/', views.recommendApi, name='recommend_api')
]