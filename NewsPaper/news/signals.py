from django.contrib.admin import action
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.core.mail import mail_admins, EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Post, Category


@receiver(m2m_changed, sender=Post.post_category.through)
def notify_subscribers(instance, action, *args, **kwargs):
    if action == 'post_add':
        html_content = render_to_string('mail_created.html', {'post_mail': instance}, )
        msg = EmailMultiAlternatives(
            subject=f'"Здравствуй, {instance.post_author}. Новая статья в твоём любимом разделе!" '
                    f'{instance.header_post}',
            body=instance.text_post[:50] + '...',
            from_email='yamargoshka@inbox.ru',
            to=['yamargoshka@inbox.ru'],
        )
        msg.attach_alternative(html_content, "text/html")

        msg.send()










