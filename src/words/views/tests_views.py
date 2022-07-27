import random

from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic.detail import DetailView

from words.models import Word, GroupOfWords, Result

from words.forms import TestInputForm, TestParametersForm

from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import FormView


def create_result_json(list_of_uuids):
    json = {"test_words": {}}
    for uuid in list_of_uuids:
        json["test_words"][f"{uuid}"] = {"input_word": None, "is_correct": None}
    return json


class TestsHomeView(TemplateView):
    template_name = "tests/tests_home.html"

    def get(self, request, *args, **kwargs):
        try:
            del request.session["test_params"]
            request.session.modified = True
        except KeyError:
            pass
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(TestsHomeView, self).get_context_data(**kwargs)
        context["form"] = TestParametersForm(self.request.user)
        return context

    def post(self, request):
        uuid = self.request.POST.getlist("groups")[0]
        kwargs = {'uuid': uuid}
        request.session['test_params'] = {}

        if request.POST.getlist("durations")[0] == "finite":
            request.session['test_params']["duration"] = "finite"
            words_qs = GroupOfWords.objects.get(id=uuid).words.all()
            list_test_words = [str(word.id) for word in words_qs]
            request.session['test_params']["list_test_words"] = list_test_words
            result = Result.objects.create(user=request.user, details=create_result_json(list_test_words))
            result.save()
            request.session["test_params"]["result_id"] = str(result.id)
        elif request.POST.getlist("durations")[0] == "loop":
            request.session['test_params']['duration'] = "loop"

        if request.POST.getlist("type")[0] == "ranked":
            request.session['test_params']["test_eval"] = "ranked"
        elif request.POST.getlist("type")[0] == "unranked":
            request.session['test_params']["test_eval"] = "unranked"

        if request.POST.getlist("test_for_translation_of")[0] == "for_w1":
            request.session["test_params"]["for_wX"] = 1
        elif request.POST.getlist("test_for_translation_of")[0] == "for_w2":
            request.session["test_params"]["for_wX"] = 2

        if request.POST.getlist("do_with_incorrect")[0] == "skip":
            request.session["test_params"]["do_with_incorrect"] = "skip"
        elif request.POST.getlist("do_with_incorrect")[0] == "repeat":
            request.session["test_params"]["do_with_incorrect"] = "repeat"

        if request.POST.getlist("lower_score_first")[0] == "lower_score_first":
            request.session["test_params"]["lower_score_first"] = "lower_score_first"
        elif request.POST.getlist("lower_score_first")[0] == "random_score_first":
            request.session["test_params"]["lower_score_first"] = "random_score_first"

        request.session['test_params']["is_ended"] = False
        request.session.modified = True
        return redirect(
            reverse_lazy("words:groups_of_words_test", kwargs=kwargs))


class GroupOfWordsTest(FormView):
    pk_url_kwarg = "uuid"
    template_name = "tests/quick_test.html"
    form_class = TestInputForm
    model = Word
    success_url = reverse_lazy("words:list")

    def get(self, request, *args, **kwargs):
        try:
            var = request.session["test_params"]
        except KeyError:
            return redirect(reverse_lazy("words:tests_home"))
        try:
            if not request.session["test_params"]['list_test_words']:
                uuid = request.session["test_params"]["result_id"]
                del request.session["test_params"]
                return redirect(reverse_lazy("words:single_result", kwargs={"uuid": uuid}))
        except KeyError:
            pass

        return self.render_to_response(self.get_context_data(req=request))

    def get_context_data(self, **kwargs):
        request = kwargs["req"]
        context = super().get_context_data(**kwargs)

        print(request.session["test_params"])

        if request.session["test_params"]["for_wX"] == 1:
            context["for_wX"] = 1
        elif request.session["test_params"]["for_wX"] == 2:
            context["for_wX"] = 2

        if request.session["test_params"]["duration"] == "finite":
            context["group_obj"] = GroupOfWords.objects.get(id=self.kwargs.get("uuid"))
            randint = random.randint(0, len(request.session["test_params"]["list_test_words"]) - 1)
            print('\n', request.session["test_params"]["list_test_words"], "\n")
            random_word_id = request.session["test_params"]["list_test_words"].pop(randint)
            request.session.modified = True
            print('\n', request.session["test_params"]["list_test_words"], "\n")
            context["word_obj"] = Word.objects.get(id=random_word_id)
            return context

        elif request.session["test_params"]["duration"] == "loop":
            context["group_obj"] = GroupOfWords.objects.get(id=self.kwargs.get("uuid"))
            if request.session["test_params"]["lower_score_first"] == "lower_score_first":
                min_score = context["group_obj"].words.filter().order_by('score').first().score
                context["word_obj"] = random.choice(context["group_obj"].words.filter(score=min_score))
            else:
                context["word_obj"] = random.choice(context["group_obj"].words.filter().order_by('score').first())
            return context

    def form_valid(self, form):
        if form.is_valid():
            word_obj = Word.objects.get(id=self.request.POST.getlist("word_obj")[0])
            input_word = self.request.POST.getlist("input_word")[0].lower().strip(" ")
            compare_with = None
            try:
                if self.request.session["test_params"]["for_wX"] == 1:
                    compare_with = word_obj.word2.lower().strip(" ")
                elif self.request.session["test_params"]["for_wX"] == 2:
                    compare_with = word_obj.word1.lower().strip(" ")
            except KeyError:
                return redirect(reverse_lazy("words:tests_home"))
            print(f"\nI COMPARE {compare_with} WITH {input_word}\n")

            if compare_with == input_word:
                messages.success(self.request,
                                 f'Answer "{input_word}" is correct. Translation of "{word_obj.word1}" is '
                                 f'"{word_obj.word2}"')
                if self.request.session["test_params"]["test_eval"] == "ranked":
                    word_obj.score += 1
                if self.request.session["test_params"]["duration"] == "finite":
                    res_obj = Result.objects.get(id=self.request.session["test_params"]["result_id"])
                    res_obj.details["test_words"][f"{str(word_obj.id)}"]["input_word"] = input_word
                    res_obj.details["test_words"][f"{str(word_obj.id)}"]["is_correct"] = True
                    res_obj.save()

            elif compare_with != input_word:
                messages.success(self.request,
                                 f'Answer "{input_word}" is incorrect. Correct translation of "{word_obj.word1}" is '
                                 f'"{word_obj.word2}"')

                if self.request.session["test_params"]["test_eval"] == "ranked":
                    word_obj.score -= 1
                if self.request.session["test_params"]["do_with_incorrect"] == "repeat" and \
                        self.request.session["test_params"]["duration"] == "finite":
                    self.request.session["test_params"]["list_test_words"].append(str(word_obj.id))
                    self.request.session.modified = True
                if self.request.session["test_params"]["duration"] == "finite":
                    res_obj = Result.objects.get(id=self.request.session["test_params"]["result_id"])
                    res_obj.details["test_words"][f"{str(word_obj.id)}"]["input_word"] = input_word
                    res_obj.details["test_words"][f"{str(word_obj.id)}"]["is_correct"] = False
                    res_obj.save()

            word_obj.save()

            return redirect(
                reverse_lazy(f"words:groups_of_words_test", kwargs={'uuid': self.kwargs["uuid"]}))


class TestsResultsListView(ListView):
    model = Result
    context_object_name = 'results'
    template_name = "tests/results_list.html"

    def get_queryset(self):
        super(TestsResultsListView, self).get_queryset()
        print(self.request.user.results)
        return self.request.user.results.all()

    def get(self, request, *args, **kwargs):
        return super(TestsResultsListView, self).get(request, *args, **kwargs)


def update_result_details():
    pass


class TestsResultView(DetailView):
    pk_url_kwarg = "uuid"
    model = Result
    context_object_name = "result"
    template_name = "tests/single_result.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        res_obj = Result.objects.get(id=self.kwargs["uuid"])
        context_dict = res_obj.generate_context_dict()
        context["dict"] = context_dict
        return context
