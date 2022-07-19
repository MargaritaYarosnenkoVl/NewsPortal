import datetime
from celery import shared_task

from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from news.models import Post, Category


@shared_task
def celery_notify_subscribers(subject, from_email, email, html_content):
    msg = EmailMultiAlternatives(
                subject=subject,
                from_email=from_email,
                to=[email]
            )

    msg.attach_alternative(html_content, "text/html")
    msg.send()


@shared_task
def celery_week_mails():
    time_delta = datetime.timedelta(7)
    start_date = datetime.datetime.utcnow() - time_delta
    end_date = datetime.datetime.utcnow()

    posts = Post.objects.filter(post_data__range=(start_date, end_date))

    for category in Category.objects.all():
        html_content = render_to_string('account/email/week_email.html',
                                        {'posts': posts, 'category': category}, )
        msg = EmailMultiAlternatives(
            subject=f'"Еженедельная подписка (celery)"',
            body="Новости",
            from_email='yamargoshka15@gmail.com',
            to=category.get_subscribers_emails())
        msg.attach_alternative(html_content, "text/html")
        msg.send()

