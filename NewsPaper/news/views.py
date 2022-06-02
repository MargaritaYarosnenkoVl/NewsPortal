from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, BaseRegisterForm
from .filters import SearchFilter
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin



class NewsList(ListView):
    model = Post
    ordering = '-id'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10


class Search(ListView):
    model = Post
    ordering = '-id'
    template_name = 'search.html'
    context_object_name = 'search'

    def get_context_data(self,
                         **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = SearchFilter(self.request.GET,
                                         queryset=self.get_queryset())
        return context


class NewsDetail(DetailView):
    model = Post
    template_name = 'news_.html'
    context_object_name = 'news_'


class NewsAdd(CreateView):
    template_name = 'add.html'
    form_class = PostForm


class NewsUpgrade(LoginRequiredMixin, UpdateView):
    template_name = 'add.html'
    form_class = PostForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class NewsDelete(DeleteView):
    template_name = 'delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'