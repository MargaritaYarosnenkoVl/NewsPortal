from django.forms import ModelForm, HiddenInput, CharField, Textarea
from django.utils.translation import gettext_lazy as _
from .models import Post, Category
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


class PostForm(ModelForm):

    header_post = CharField(label='Заголовок', min_length=5)
    text_post = CharField(label='Статья', min_length=10, widget=Textarea)

    class Meta:
        model = Post
        fields = ['post_author', 'header_post', 'news_post', 'post_category', 'text_post']
        labels = {
            'news_post': _('Тип'),
            'post_category': _('Категория'),
            'post_author': _('Автор'),
        }


class CommonSignupForm(SignupForm):

    def save(self, request):
        user = super(CommonSignupForm, self).save(request)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)
        return user