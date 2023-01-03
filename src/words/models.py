from django.db import models
import uuid
from googletrans import Translator
from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import CustomUser

import random

from faker import Faker


class Word(models.Model):
    user = models.ForeignKey(to=CustomUser, related_name="words", related_query_name='words', on_delete=models.CASCADE)
    word1 = models.CharField(max_length=50)
    word2 = models.CharField(max_length=50)
    id = models.UUIDField(default=uuid.uuid4, db_index=True, unique=True, editable=False, primary_key=True)
    score = models.IntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.word1}: {self.word2}"

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

    # @classmethod
    # def generate(cls, num):
    #     faker = Faker()
    #     for _ in range(1, num):
    #         translator = Translator()
    #         word1 = faker.word()
    #         tr = translator.translate(str(word1), src="en", dest="ru")
    #         word2 = tr.text
    #         wordobj = Word(word1=f"{word1}", word2=f"{word2}")
    #         wordobj.user = CustomUser.objects.get(username="admin")
    #         wordobj.score = random.randint(-10, 50)
    #         wordobj.save()
    #         # wordobj.group.add(random.choice(list(wordobj.user.groups_of_words.all())))
    #         wordobj.group.add(wordobj.user.groups_of_words.get(name="General"))
    #         wordobj.save()


# class GroupOfWordsManager(models.Manager):
#     def get_queryset(self):
#         return super().get_queryset().exclude(name='General')


class GroupOfWords(models.Model):
    id = models.UUIDField(default=uuid.uuid4, db_index=True, unique=True, editable=False, primary_key=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200, null=True, blank=True)
    words = models.ManyToManyField(to=Word, related_name='groups', related_query_name='groups', null=True, blank=True)
    user = models.ForeignKey(to=CustomUser, related_name="groups_of_words", on_delete=models.CASCADE, null=False,
                             editable=False)

    # objects = GroupOfWordsManager()

    def __repr__(self):
        return f"{self.name}"

    def __str__(self):
        return f"{self.name}"


@receiver(post_save, sender=Word)
def custom_word(instance, created, **kwargs):
    if created:
        print(f"Word instance created: '{instance}'")


# class TestOptions(models.Model):
#     group = models.(to=GroupOfWords, on_delete=models.CASCADE)


class Result(models.Model):
    DURATION = (('finite', 'Test will end after all words are examined'),
                ('infinite', 'Test will run looped until you decide to finish'))
    SCORING_TYPE = (('ranked', 'Every mistake or success is counted'),
                    ('unranked', 'Results do not affect words\' scores'))
    EXAMINE_WORD_NUMBER = (('1', 'Word to translation'),
                           ('2', 'Translation to word'),
                           # ('mixed', 'Mixed')
                           )
    DO_WITH_INCORRECT = (('skip', 'Go next if a mistake is made'),
                         ('repeat', 'Reask until answer is correct'))
    WHICH_GOES_FIRSTLY = (('random', 'Random words are asked'),
                          ('lower_score', 'Words with lower score asked firstly'))
    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE, related_name="results")
    groups = models.ManyToManyField(to=GroupOfWords, related_name='results',
                                    related_query_name='results')
    duration = models.CharField(choices=DURATION, max_length=50)
    scoring_type = models.CharField(choices=SCORING_TYPE, max_length=50)
    word2examine_number = models.CharField(choices=EXAMINE_WORD_NUMBER, max_length=50, verbose_name="Testing type")
    do_with_incorrect = models.CharField(choices=DO_WITH_INCORRECT, max_length=50, verbose_name="Incorrect answer")
    which_goes_first = models.CharField(choices=WHICH_GOES_FIRSTLY, max_length=50, verbose_name="Word order")
    id = models.UUIDField(default=uuid.uuid4, db_index=True, unique=True, editable=False, primary_key=True)
    current_words = models.JSONField(default=dict)
    details = models.JSONField(default={'fnl_res_4test_words': []})
    # options = models.ForeignKey(to=TestOptions, on_delete=models.CASCADE)
    ended = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def generate_context_dict(self):
        context_dict = {"fnl_res_4test_words": {}}
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
