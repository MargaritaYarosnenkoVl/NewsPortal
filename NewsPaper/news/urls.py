from django.urls import path
# Импортируем созданное нами представление
from .views import NewsList, NewsDetail, Search, NewsEdit, NewsDelete

urlpatterns = [
    path('', NewsList.as_view()),
    path('<int:pk>', NewsDetail.as_view(), name='news_'),
    path('search/', Search.as_view(), name='search'),
    path('add/', Search.as_view(), name='add'),
    path('<int:pk>/edit', NewsEdit.as_view(), name='edit'),
    path('<int:pk>/delete', NewsDelete.as_view(), name='delete'),
]
