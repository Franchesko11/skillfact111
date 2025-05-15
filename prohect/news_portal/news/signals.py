from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import News
from .tasks import send_news_notification

@receiver(post_save, sender=News)
def news_created(sender, instance, created, **kwargs):
    if created:
        send_news_notification.delay(instance.id)