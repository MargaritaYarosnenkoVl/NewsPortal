from django.forms import ModelForm, HiddenInput, CharField, Textarea

from django.utils.translation import gettext_lazy as _
from .models import Post


class PostForm(ModelForm):
    header_post = CharField(label='Заголовок', min_length=5)
    text_post = CharField(label='Статья', min_length=10, widget=Textarea)

    class Meta:
        model = Post
        fields = ['post_author', 'header_post', 'text_post', 'news_post', 'post_category']
        widgets = {
            'post_author': HiddenInput(),
        }
        labels = {
            'news_post': _('Тип'),
        }
