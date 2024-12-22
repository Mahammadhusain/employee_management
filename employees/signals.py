from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import User

@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created and instance.role == 'employee':
        send_mail(
            subject="Welcome to the Company",
            message="Welcome to the company, {}".format(instance.name),
            from_email="host@email.com",
            recipient_list=[instance.email],
        )
