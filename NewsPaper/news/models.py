from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum



class Author(models.Model):
    author_user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating_author = models.IntegerField(default=0)

    def update_rating(self):
        sum_rating_author = self.post_set.all().aggregate(Sum('rating_post'))['rating_post__sum'] * 3
        sum_rating_comment = self.author_user.comment_set.all().aggregate(Sum('rating_comment'))['rating_comment__sum']
        sum_rating = self.post_set.all().aggregate(Sum('comment__rating_comment'))['comment__rating_comment__sum']
        self.rating_author = sum_rating_author + sum_rating_comment + sum_rating
        self.save()


class Category(models.Model):
    name_category = models.CharField(max_length=255, unique=True)


class Post(models.Model):
    article = 'ar'
    news = 'nw'

    NEWS_POST = [
        (article, 'Статья'),
        (news, 'Новость'),
    ]

    post_author = models.ForeignKey(Author, on_delete=models.CASCADE)
    news_post = models.CharField(max_length=2, choices=NEWS_POST, default=article)
    post_data = models.DateField(auto_now_add=True)
    header_post = models.CharField(max_length=255)
    text_post = models.TextField()
    rating_post = models.IntegerField(default=0)

    post_category = models.ManyToManyField(Category, through='PostCategory')

    def like(self):
        self.rating_post += 1
        self.save()

    def dislike(self):
        self.rating_post -= 1
        self.save()

    def preview(self):
        return self.text_post[:124] + '...'

    def __str__(self):
        return f'{self.header_post, n/self.post_data, self.text_post}'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE)
    text_comment = models.TextField()
    comment_data = models.DateField(auto_now_add=True)
    rating_comment = models.IntegerField(default=0)

    def like(self):
        self.rating_comment += 1
        self.save()

    def dislike(self):
        self.rating_comment -= 1
        self.save()

