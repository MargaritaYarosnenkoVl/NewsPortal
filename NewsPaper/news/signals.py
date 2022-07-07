from django.contrib.admin import action
from django.contrib.auth.models import User
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
        users_emails = [
                user.email
                for category in instance.post_category.all()
                for user in category.subscribers.all()
            ]
        for email in users_emails:
            user = User.objects.get(email=email)
            html_content = render_to_string('mail_created.html', {'post_mail': instance}, )
            msg = EmailMultiAlternatives(
                subject=f'"Здравствуй, {user.username}. Новая статья в твоём любимом разделе!"'
                        f'{instance.header_post}',
                body=instance.text_post[:50] + '...',
                from_email='yamargoshka@inbox.ru',
                to=[email]
                )
            msg.attach_alternative(html_content, "text/html")
            msg.send()


@receiver(pre_save, sender=Post)
def limitation_post(sender, instance, **kwargs):
    quantity_posts = sender.objects.filter(post_author=instance.post_author, post_data__date=datetime.datetime.now().date())
    print('мой вывод', len(quantity_posts))
    return len(quantity_posts)











