from django_filters import FilterSet
from .models import Post


# создаём фильтр
class SearchFilter(FilterSet):
    class Meta:
        model = Post
        fields = ('post_data', 'header_post', 'post_author')