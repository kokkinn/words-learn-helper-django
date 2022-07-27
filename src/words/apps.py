from django.apps import AppConfig
from django.db.models.signals import post_save
from django.dispatch import receiver


class WordsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'words'


@receiver(post_save, sender='words.Word')
def word_creation_dispatcher(created, instance, **kwargs):
    if created:
        print('\nAAAAAAAAALALALALALALALALAL\n')
        user = instance.user
        user.general_group.words.add(instance)
