from django.contrib import admin
from .models import Author, Category, Post, PostCategory, Comment


'''class AuthorAdmin(admin.ModelAdmin):

    list_display = ('author_user', 'rating_author')
    list_filter = ('author_user')
    search_fields = ('author_user')'''


admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(PostCategory)
admin.site.register(Comment)
