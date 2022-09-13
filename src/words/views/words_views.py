from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import redirect
from django.views.generic.detail import SingleObjectMixin

from words.filters import WordFilter
from words.models import Word

from words.forms import WordForm

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from django.views.generic.edit import UpdateView


class WordsListView(LoginRequiredMixin, ListView):
    context_object_name = "words"
    model = Word
    template_name = "words/list.html"

    def get_queryset(self):
        super(WordsListView, self).get_queryset()
        return self.request.user.words.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter"] = WordFilter(self.request.GET, queryset=self.get_queryset(), request=self.request)
        filtered_word_qs = context["filter"].qs
        print(filtered_word_qs)
        if filtered_word_qs:
            context["total"] = filtered_word_qs.count()
            context["min"] = filtered_word_qs.order_by("score").first().score
            context["max"] = filtered_word_qs.order_by("score").last().score
            context["avg"] = round(Word.average_score(self.request.user, qs=filtered_word_qs), 2)
        return context

    def get_template_names(self):
        super().get_template_names()
        if not self.request.user.words.all():
            return ["words/no_words.html"]
        else:
            return ["words/list.html"]

    def post(self, request):
        if "delete_button" in request.POST:
            checks = request.POST.getlist("checks")
            for checked_word_id in checks:
                Word.objects.get(id=checked_word_id).delete()
            return redirect(reverse_lazy("words:list"))


class WordUpdateView(LoginRequiredMixin, UpdateView, SingleObjectMixin):
    pk_url_kwarg = 'uuid'
    model = Word
    form_class = WordForm
    template_name = "words/word_form.html"
    success_url = reverse_lazy("words:list")

    # def __init__(self):
    #     super(WordUpdateView, self).__init__()

    def get(self, request, *args, **kwargs):
        try:
            Word.objects.get(user=self.request.user, id=self.kwargs["uuid"])
        except Word.DoesNotExist:
            raise Http404
        return super(WordUpdateView, self).get(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(WordUpdateView, self).get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def form_valid(self, form):

        if form.is_valid():
            word = Word.objects.get(id=self.kwargs["uuid"])
            word.group.clear()
            word.save()
            for group in form.cleaned_data["groups"]:
                group.words.add(word)
        form.save()
        messages.success(self.request, f"Pair {form.instance.word1} - {form.instance.word2} updated")
        return super().form_valid(form)

    def get_initial(self):
        initial = super(WordUpdateView, self).get_initial()
        initial["groups"] = Word.objects.get(id=self.kwargs["uuid"]).group.all()
        return initial

    def get_context_data(self, **kwargs):
        context = super(WordUpdateView, self).get_context_data()
        context["type"] = "update"
        return context


class WordCreateView(LoginRequiredMixin, CreateView):
    model = Word
    form_class = WordForm
    template_name = "words/word_form.html"
    success_url = reverse_lazy("words:create")

    def get_form_kwargs(self):
        kwargs = super(WordCreateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        print(form)
        print(self.request.POST)
        if form.is_valid():
            form.instance.user = self.request.user
            form.save()
            for group in form.cleaned_data["groups"]:
                group.words.add(form.instance)
        form.save()
        messages.success(self.request, f"Pair '{form.instance.word1} - {form.instance.word2}' created")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(WordCreateView, self).get_context_data()
        context["type"] = "create"
        no_groups = False
        if len(self.request.user.groups_of_words.all()) == 1:
            no_groups = True
        context['no_groups'] = no_groups

        return context


@login_required
def home_view(request):
    return render(request, "words/home.html")


@login_required
def one_word_view(request, uuid):
    word = Word.objects.get(id=uuid)
    context = {"word": word}
    return render(request, "words/single_word.html", context)


@login_required
def delete_view(request, uuid):
    try:
        Word.objects.get(user=request.user, id=uuid)
    except Word.DoesNotExist:
        raise Http404
    word_object = Word.objects.get(id=uuid)
    # if request.method == "POST":
    word_object.delete()
    messages.success(request, f"Pair '{word_object.word1} - {word_object.word2}' deleted")
    return redirect(reverse_lazy("words:list"))

    # return render(request, "words/delete.html", context)
