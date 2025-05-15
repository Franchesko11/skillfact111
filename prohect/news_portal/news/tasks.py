from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from datetime import timedelta
from .models import News, Subscription


@shared_task
def send_news_notification(news_id):
    news = News.objects.get(id=news_id)
    subscribers = Subscription.objects.filter(category=news.category)

    for subscriber in subscribers:
        subject = f'Новая новость в категории {news.category.name}'
        message = render_to_string('news/email_notification.html', {
            'news': news,
            'subscriber': subscriber.user,
        })
        send_mail(
            subject=subject,
            message='',
            html_message=message,
            from_email='admin@newssite.com',
            recipient_list=[subscriber.user.email],
            fail_silently=False,
        )


@shared_task
def send_weekly_newsletter():
    
    week_ago = timezone.now() - timedelta(days=7)


    categories = Category.objects.all()

    for category in categories:

        recent_news = News.objects.filter(
            category=category,
            publish_date__gte=week_ago
        ).order_by('-publish_date')[:5]

        if recent_news.exists():
            subscribers = Subscription.objects.filter(category=category)

            for subscriber in subscribers:
                subject = f'Еженедельная рассылка новостей: {category.name}'
                message = render_to_string('news/weekly_newsletter.html', {
                    'category': category,
                    'news_list': recent_news,
                    'subscriber': subscriber.user,
                })
                send_mail(
                    subject=subject,
                    message='',
                    html_message=message,
                    from_email='admin@newssite.com',
                    recipient_list=[subscriber.user.email],
                    fail_silently=False,
                )