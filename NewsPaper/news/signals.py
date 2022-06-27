from django.contrib.admin import action
from django.db.models import Count
from django.db.models.signals import post_save, m2m_changed, pre_save
from django.dispatch import receiver
from django.core.mail import mail_admins, EmailMultiAlternatives
from django.template.loader import render_to_string
import datetime


from .models import Post, Category


@receiver(m2m_changed, sender=Post.post_category.through)
def notify_subscribers(instance, action, *args, **kwargs):
    if action == 'post_add':
        html_content = render_to_string('mail_created.html', {'post_mail': instance}, )
        msg = EmailMultiAlternatives(
            subject=f'"Здравствуй, {instance.post_author}. Новая статья в твоём любимом разделе!"'
                    f'{instance.header_post}',
            body=instance.text_post[:50] + '...',
            from_email='yamargoshka@inbox.ru',
            to={
                user.email
                for category in instance.post_category.all()
                for user in category.subscribers.all()
            })
        msg.attach_alternative(html_content, "text/html")

        msg.send()


@receiver(pre_save, sender=Post)
def limitation_post(sender, instance, **kwargs):
    quantity_posts = sender.objects.filter(post_author=instance.post_author, post_data=instance.post_data)
    posts = Count('quantity_posts')
    return instance.posts


