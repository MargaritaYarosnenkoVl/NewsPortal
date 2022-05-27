from django.urls import path
# Импортируем созданное нами представление
from .views import NewsList, NewsDetail, Search


urlpatterns = [
    path('', NewsList.as_view()),
    path('<int:pk>', NewsDetail.as_view()),
    path('/search/', Search.as_view()),
]
