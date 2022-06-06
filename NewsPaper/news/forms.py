from django.forms import ModelForm, HiddenInput, CharField, Textarea
from django.utils.translation import gettext_lazy as _
from .models import Post
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from django import forms


class PostForm(ModelForm):
    header_post = CharField(label='Заголовок', min_length=5)
    text_post = CharField(label='Статья', min_length=10, widget=Textarea)

    class Meta:
        model = Post
        fields = ['header_post', 'news_post', 'post_category', 'text_post']
        widgets = {
            'post_author': forms.HiddenInput(),
        }
        labels = {
            'news_post': _('Тип'),
            'post_category': _('Категория'),
        }


class CommonSignupForm(SignupForm):
    def save(self, request):
        user = super(CommonSignupForm, self).save(request)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)
        return user
