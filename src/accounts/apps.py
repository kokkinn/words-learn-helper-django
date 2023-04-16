from django.apps import AppConfig
from django.db.models.signals import post_save

from django.dispatch import Signal, receiver
import django

from .utils import send_activation_notification


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'


user_registered = Signal()


def user_registered_dispatcher(**kwargs):
    send_activation_notification(kwargs['instance'])


user_registered.connect(user_registered_dispatcher)


@receiver(post_save, sender='accounts.CustomUser')
def user_creation_dispatcher(instance, created, **kwargs):
    from words.models import GroupOfWords
    django.setup()
    if created:
        
        gen_gro = GroupOfWords.objects.create(name="General", user=instance)
        gen_gro.save()
        instance.general_group = gen_gro
        instance.save()
