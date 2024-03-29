from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Post, Author
from .filters import SearchFilter
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
#from .signals import limitation_post
from django.core.cache import cache



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
    paginate_by = 10

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

    def get_context_data(self,
                         **kwargs):
        context = super().get_context_data(**kwargs)
        categories = self.object.post_category.all()
        is_subscriber = False
        #is_subscriber = {categories.get(id): False}

        for cat in categories:
            if self.request.user in cat.subscribers.all():
                is_subscriber = True
                break

        context['subscribers'] = is_subscriber
        return context

    def get_object(self, **kwargs):
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)

        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)

        return obj


class NewsAdd(PermissionRequiredMixin, CreateView):
    model = Post
    template_name = 'add.html'
    form_class = PostForm
    permission_required = ('news.add_post')

    def post(self, request, *args, **kwargs):
        post_mail = Post(post_author=Author.objects.get(author_user=self.request.user),
                         news_post=request.POST.get('news_post'),
                         header_post=request.POST.get('header_post'),
                         text_post=request.POST.get('text_post'))

        #if limitation_post(sender=Post, instance=post_mail, **kwargs) < 10000000:
        post_mail.save()
        post_mail.post_category.add(*request.POST.getlist('post_category'))
        #else:
            #print('Нельзя создавать больше 3х статей за день')

        return redirect('/')


    def form_valid(self, form):
        user = self.request.user
        self.object = form.save(commit=False)
        self.object.post_author = Author.objects.get(author_user=user)
        self.object.save()
        return super().form_valid(form)


class NewsDelete(DeleteView):
    template_name = 'delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'


class NewsUpgrade(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'add.html'
    form_class = PostForm
    permission_required = ('news.change_post')

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
        Author.objects.create(author_user=user)
    return redirect('/')


@login_required
def subscribe(request, **kwargs):
    post = Post.objects.get(pk=kwargs['pk'])
    user = request.user
    for category in post.post_category.all():
        if user not in category.subscribers.all():
            category.subscribers.add(user)

    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def unsubscribe(request, **kwargs):
    post = Post.objects.get(pk=kwargs['pk'])
    user = request.user
    for category in post.post_category.all():
        if user in category.subscribers.all():
            category.subscribers.remove(user)

    return redirect(request.META.get('HTTP_REFERER', '/'))



