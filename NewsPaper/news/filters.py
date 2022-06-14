from django.forms import SelectDateWidget
from django_filters import FilterSet, DateFilter, CharFilter
from .models import Post


class SearchFilter(FilterSet):
    post_data = DateFilter(field_name='post_data', lookup_expr='gt', label='Опубликовано после',
                           widget=SelectDateWidget)
    header_post = CharFilter(field_name='header_post', label='Заголовок')


    class Meta:
        model = Post
        fields = ('post_author', 'header_post', 'post_data', 'post_category')

