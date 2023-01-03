import random

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic.detail import DetailView

from words.models import Word, Result

from words.forms import TestInputForm, TestParametersForm

from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import FormView, CreateView


class TestsHomeView(LoginRequiredMixin, CreateView):
    template_name = "tests/home.html"
    form_class = TestParametersForm
    model = Result

    def get_form_kwargs(self):
        kwargs = super(TestsHomeView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_initial(self):
        initial = super(TestsHomeView, self).get_initial()
        initial['groups'] = self.request.user.groups_of_words.filter(name='General').all()
        initial['duration'] = 'finite'
        initial['scoring_type'] = 'ranked'
        initial['word2examine_number'] = 1
        initial['do_with_incorrect'] = 'skip'
        initial['which_goes_first'] = 'random'
        return initial

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        words4test = None
        if form.instance.which_goes_first == 'random':  # set up an order of a words "que"
            words4test = [str(word.id) for word in
                          Word.objects.none().union(*[group.words.all()
                                                      for group in form.instance.groups.all()])]
        elif form.instance.which_goes_first == 'lower_score':
            words4test = [str(word.id) for word in
                          Word.objects.none().union(*[group.words.all()
                                                      for group in form.instance.groups.all()]).order_by('score')]
        form.instance.current_words = {'words4test': words4test,
                                       'current_word': dict()
                                       }
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('words:test-question', kwargs={'uuid': self.object.id})


def qs_from_uuid_list(list_):
    return Word.objects.filter(id__in=list_)


def word_obj_from_id(id_):
    return Word.objects.get(id=id_)


class TestQuestionView(LoginRequiredMixin, FormView):
    pk_url_kwarg = "uuid"
    template_name = "tests/test_question.html"
    form_class = TestInputForm
    model = Result

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.result_object = None
        self.word_object = None

    def dispatch(self, request, *args, **kwargs):
        self.result_object = Result.objects.get(id=self.kwargs.get('uuid'))

        if not self.result_object.current_words['words4test'] and self.result_object.duration == 'finite':
            return redirect(
                reverse_lazy('words:single_result', kwargs={'uuid': self.result_object.id}))  # finish test check

        if self.result_object.current_words['current_word'] == dict():
            # if there is no current word (start of test or next word, but not a repeated word),
            # pick a new word, assign it to VIEW attribute (self) and to Result model info field
            def set_info():
                self.result_object.current_words['current_word']['id'] = str(self.word_object.id)
                self.result_object.current_words['current_word']['ask'] = \
                    self.word_object.word1 if self.result_object.word2examine_number == '1' else self.word_object.word2
                self.result_object.current_words['current_word']['ans'] = \
                    self.word_object.word2 if self.result_object.word2examine_number == '1' else self.word_object.word1

            if self.result_object.which_goes_first == 'random':
                random_int = random.randint(0, len(self.result_object.current_words['words4test']) - 1)
                self.word_object = word_obj_from_id(self.result_object.current_words['words4test'][random_int])
                set_info()

            elif self.result_object.which_goes_first == 'lower_score':  # take one with the lowest score (1st in ordered)
                self.word_object = word_obj_from_id(self.result_object.current_words['words4test'][0])
                set_info()

        else:
            self.word_object = word_obj_from_id(self.result_object.current_words['current_word']['id'])
        self.result_object.save()
        return super().dispatch(request, *args, **kwargs)

    # def get(self, request, *args, **kwargs):
    #
    #
    #
    #     return super(TestQuestionView, self).get(self, request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(TestQuestionView, self).get_context_data(**kwargs)
        context['word2examine'] = self.result_object.current_words['current_word']['ask']
        return context

    def form_valid(self, form):

        def append_info(is_cor: bool):
            if self.result_object.scoring_type == 'ranked':
                if is_cor:
                    self.word_object.score += 1
                else:
                    self.word_object.score -= 1

            self.result_object.details['fnl_res_4test_words'].append({
                'pair': f"{self.word_object.word1} : {self.word_object.word2}",
                'user_input': user_input,
                'is_correct': is_cor
            })

        user_input = form.cleaned_data['input_word']

        if user_input == self.result_object.current_words['current_word']['ans']:
            messages.success(message='The answer is correct', request=self.request)
            append_info(True)
            self.result_object.current_words['current_word'] = dict()
            if self.result_object.duration == 'finite':
                self.result_object.current_words['words4test'].remove(str(self.word_object.id))

        elif user_input != self.result_object.current_words['current_word']['ans']:
            messages.error(message='The answer is incorrect', request=self.request)
            append_info(False)
            if self.result_object.do_with_incorrect == 'skip':
                self.result_object.current_words['current_word'] = dict()
                if self.result_object.duration == 'finite':
                    self.result_object.current_words['words4test'].remove(str(self.word_object.id))
        self.word_object.save()
        self.result_object.save()
        return redirect(reverse_lazy('words:test-question', kwargs={'uuid': self.result_object.id}))


class ResultsListView(LoginRequiredMixin, ListView):
    model = Result
    context_object_name = 'results'
    template_name = "tests/list.html"

    def get_queryset(self):
        super(ResultsListView, self).get_queryset()
        return self.request.user.results.all().order_by('-date')

    def get_template_names(self):
        super().get_template_names()
        if not self.request.user.results.all():
            return ["tests/no_results.html"]
        else:
            return ["tests/list.html"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_words_qs = self.request.user.words.all()
        # context["total"] = user_words_qs.count()
        context["min"] = user_words_qs.order_by("score").first().score
        context["max"] = user_words_qs.order_by("score").last().score
        context["avg"] = round(Word.average_score(self.request.user, qs=user_words_qs), 2)
        return context


def update_result_details():
    pass


class TestsResultView(LoginRequiredMixin, DetailView):
    pk_url_kwarg = "uuid"
    model = Result
    context_object_name = "result"
    template_name = "tests/single.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["fnl_res_4test_words"] = self.object.details['fnl_res_4test_words']
        return context
