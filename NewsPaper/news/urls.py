from django.urls import path
from .views import NewsList, NewsDetail, Search, NewsUpgrade, NewsDelete, NewsAdd, upgrade_me
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', NewsList.as_view()),
    path('<int:pk>', NewsDetail.as_view(), name='news_'),
    path('search/', Search.as_view(), name='search'),
    path('add/', NewsAdd.as_view(), name='add'),
    path('<int:pk>/edit', NewsUpgrade.as_view(), name='edit'),
    path('<int:pk>/delete', NewsDelete.as_view(), name='delete'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('upgrade/', upgrade_me, name='upgrade')
]
