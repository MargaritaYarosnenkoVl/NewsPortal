from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Post, Author, Category
from .filters import SearchFilter
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string


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


class NewsAdd(PermissionRequiredMixin, CreateView):
    model = Post
    template_name = 'add.html'
    form_class = PostForm
    permission_required = ('news.add_post')

    def form_valid(self, form):
        user = self.request.user
        self.object = form.save(commit=False)
        self.object.post_author = Author.objects.get(author_user=user)
        self.object.save()
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        post_mail = Post(post_author=request.POST('post_author'),
                         news_post=request.POST('news_post'),
                         header_post=request.POST('header_post'),
                         text_post=request.POST('text_post'),
                         post_category=request.POST('post_category'))
        post_mail.save()

        html_content = render_to_string(
            'mail_created.html',
            {
                'post_mail': post_mail,
            }
        )

        msg = EmailMultiAlternatives(
            subject=f'"Здравствуйте, {post_mail.post_author} Новая статья в твоём любимом разделе!"',
            body=post_mail.text_post[:50] + "...",
            from_email='YaMargoshka@yandex.ru',
            to=['YaMargoshka@yandex.ru'])

        msg.attach_alternative(html_content, "text/html")

        msg.send()

        return redirect('post_mail:post_mail')


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
def subscribe(request,  *args, **kwargs):
    pass
