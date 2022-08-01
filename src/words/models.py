from django.db import models
import uuid
from googletrans import Translator
from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import CustomUser

import random

from faker import Faker


class GroupOfWords(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200, null=True, blank=True)
    id = models.UUIDField(default=uuid.uuid4, db_index=True, unique=True, editable=False, primary_key=True)
    user = models.ForeignKey(to=CustomUser, related_name="groups_of_words", on_delete=models.CASCADE, null=False)

    def __str__(self):
        return f"{self.name}, {self.user}"


class Word(models.Model):
    user = models.ForeignKey(to=CustomUser, related_name="words", on_delete=models.CASCADE)
    word1 = models.CharField(max_length=30)
    word2 = models.CharField(max_length=30)
    id = models.UUIDField(default=uuid.uuid4, db_index=True, unique=True, editable=False, primary_key=True)
    score = models.IntegerField(default=0)
    group = models.ManyToManyField(to=GroupOfWords, related_name='words', blank=True, null=True)

    #
    # def __init__(self):
    #     if
    #     super(Word, self).__init__()

    def __str__(self):
        return f"{self.word1}: {self.word2}, {self.score}, {str(self.id)[0:4]}"


    # def try_get_list_from_word(self):



    @classmethod
    def average_score(cls, user, qs=None):
        score_counter = 0
        if qs:
            total_words = qs.all().count()
            for word in qs:
                score_counter += word.score
        else:
            total_words = user.words.all().count()
            for word in user.words.all():
                score_counter += word.score
        return score_counter / total_words

    @classmethod
    def generate(cls, num):
        faker = Faker()
        for _ in range(1, num):
            translator = Translator()
            word1 = faker.word()
            tr = translator.translate(str(word1), src="en", dest="ru")
            word2 = tr.text
            wordobj = Word(word1=f"{word1}", word2=f"{word2}")
            wordobj.user = CustomUser.objects.get(username="admin")
            wordobj.score = random.randint(-10, 50)
            wordobj.save()
            # wordobj.group.add(random.choice(list(wordobj.user.groups_of_words.all())))
            wordobj.group.add(wordobj.user.groups_of_words.get(name="General"))
            wordobj.save()


@receiver(post_save, sender=Word)
def custom_word(instance, created, **kwargs):
    if created:
        print(f"Word instance created: '{instance}'")


class Result(models.Model):
    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE, related_name="results")
    id = models.UUIDField(default=uuid.uuid4, db_index=True, unique=True, editable=False, primary_key=True)
    details = models.JSONField(default=dict)
    ended = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def generate_context_dict(self):
        context_dict = {"test_words": {}}
        dict_details = self.details
        for key in list(dict_details["test_words"].keys()):
            try:
                context_dict["test_words"][f'{Word.objects.get(id=key).word1} - {Word.objects.get(id=key).word2}'] = \
                    dict_details["test_words"][key]
            except:
                context_dict["test_words"]["Word was deleted"] = dict_details["test_words"][key]
                self.details["test_words"]["Word was deleted"] = dict_details["test_words"][key]
                del self.details["test_words"][key]
                self.save()
        return context_dict
