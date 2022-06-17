from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import mail_managers

from .models import Post


@receiver(post_save, sender=Post)
def notify_subscribers(instance, created, *args, **kwargs):
    if created:
        subject = f'{instance.post_author} '
    else:
        subject = f'Изменения для {instance.post_author}'

    mail_managers(
        subject=(f'{Post.post_author}, Привет')
    )
