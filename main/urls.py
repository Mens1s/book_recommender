from django.urls import path
from . import views

urlpatterns = [
    path('get_books/', views.get_books, name='get_books'),
    path('get_book_info/<str:book_name>/', views.get_book_info, name='get_book_specific'),
    path('get_book_info/get_books/', views.get_books, name='get_books_spesific'),
    path("popular.html", views.popular, name = "popular"),
    path("recommend.html", views.recommend, name = "recommend"),
    path("index.html", views.main, name = "main"),
    path("scanbook.html", views.scanbook, name = "scanbook"),
    path("recommended_book", views.recommend_book, name = "recommend_book"),
    path("api/esp/", views.esp, name = "esp"),
    path("", views.main, name = "main"),
    path('api/recommend/', views.recommendApi, name='recommend_api')
]