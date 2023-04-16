import json
import random

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, JsonResponse
from django.shortcuts import redirect
from django.views.generic.detail import SingleObjectMixin

import words.models
from accounts.models import CustomUser
from words.filters import WordFilter
from words.models import Word, GroupOfWords
from django.db.models import Q

from words.forms import WordCUForm

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from django.views.generic.edit import UpdateView

from words.utils import json_response_form_errors, is_ajax


class WordsListView(LoginRequiredMixin, ListView):
    context_object_name = "words"
    model = Word
    template_name = "words/list.html"

    def get_queryset(self):
        qs = self.request.user.words.all()
        if self.request.GET.getlist('groups'):
            for group in self.request.GET.getlist('groups'):
                qs = qs.filter(groups__id=group)

        if self.request.GET.get('search'):
            qs = qs.filter(
                Q(word1__icontains=self.request.GET.get('search')) | Q(
                    word2__icontains=self.request.GET.get('search'))).all()

        return qs.order_by('-created_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['groups_for_create'] = self.request.user.groups_of_words.exclude(
            id=self.request.user.general_group.id).all()
        context['search'] = self.request.GET.get('search', default='')
        context['form'] = WordCUForm(request=self.request)
        context['word1_form'] = self.request.GET.get('word1_form', default='')
        context['word2_form'] = self.request.GET.get('word2_form', default='')
        context["filter"] = WordFilter(self.request.GET,
                                       queryset=self.get_queryset(),
                                       request=self.request)
        context['chosen_groups'] = self.request.GET.getlist('groups', default='')

        return context

    def get_template_names(self):
        super().get_template_names()
        if not self.request.user.words.all():
            return ["words/no_words.html"]
        else:
            return ["words/list.html"]


def id_2_name(id_):
    return GroupOfWords.objects.get(id=id_).name


class WordCreateView(LoginRequiredMixin, CreateView):
    model = Word
    form_class = WordCUForm
    template_name = "words/word_CU_form.html"
    success_url = reverse_lazy('words:list')

    def get_form_kwargs(self):
        kwargs = super(WordCreateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        if form.is_valid():
            
            form.instance.user = self.request.user
            form.save()
            for group in form.cleaned_data["groups"]:
                form.instance.groups.add(group)
            word_instance = form.save()
            if is_ajax(self.request):
                ser_word = json.dumps({"pk": str(word_instance.id),
                                       "word1": word_instance.word1,
                                       "word2": word_instance.word2,
                                       "score": "0",
                                       "groups": [group.name for group in word_instance.groups.exclude(
                                           id=self.request.user.general_group.id).all()]
                                       })
                return JsonResponse({"instance": ser_word, "status": json.dumps("form_valid")}, status=200)
            return super().form_valid(form)

    def form_invalid(self, form):
        if is_ajax(self.request):
            return json_response_form_errors(form=form)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(WordCreateView, self).get_context_data()
        context["type"] = "create"
        if not self.request.user.groups_of_words.exclude(
                id=self.request.user.general_group.id):
            context['user_has_groups'] = 0
        else:
            context['user_has_groups'] = 1

        return context


class WordUpdateView(LoginRequiredMixin, UpdateView, SingleObjectMixin):
    pk_url_kwarg = 'uuid'
    model = Word
    form_class = WordCUForm
    template_name = "words/word_CU_form.html"
    success_url = reverse_lazy("words:list")

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
            word_obj = self.object
            word_obj.groups.clear()
            for group_uuid in self.request.POST.getlist('groups[]') or self.request.POST.getlist('groups'):
                word_obj.groups.add(GroupOfWords.objects.get(id=group_uuid))
            word_obj.groups.add(self.request.user.general_group)
            word_obj.save()
            if is_ajax(self.request):
                return JsonResponse({'status': json.dumps('form_valid')}, status=200)
            return super().form_valid(form)

    def form_invalid(self, form):
        return json_response_form_errors(form=form)

    def get_initial(self):
        initial = super(WordUpdateView, self).get_initial()
        initial["groups"] = Word.objects.get(id=self.kwargs["uuid"]).groups.all()  # initial data for a form field
        
        return initial

    def get_context_data(self, **kwargs):
        context = super(WordUpdateView, self).get_context_data()
        context["type"] = "update"
        if self.request.user.groups_of_words.exclude(
                id=self.request.user.general_group.id) != GroupOfWords.objects.none():
            context['user_has_groups'] = 1
        else:
            context['user_has_groups'] = 0

        return context


@login_required
def get_initial_groups_of_word(request):
    init_groups = Word.objects.get(id=request.GET.get('word_id')).groups.all()
    all_user_groups = CustomUser.objects.get(id=request.GET.get('user_id')).groups_of_words.all()
    res = json.dumps(
        {"GoW_forWord_info":
            [
                {'id': str(group.id), 'name': group.name, 'is_init': 1} if group in init_groups
                else {'id': str(group.id), 'name': group.name, 'is_init': 0}
                for group in all_user_groups
            ]
        }
    )

    return JsonResponse({"data": res}, status=200)


@login_required
def home_view(request):
    return render(request, "words/menu.html")


@login_required
def delete_view(request, uuid):
    
    if is_ajax(request=request) and request.method == 'POST':
        
        try:
            word_object = Word.objects.get(user=request.user, id=uuid)
        except Word.DoesNotExist:
            raise Http404
        word_object.delete()
        return JsonResponse(data={'state': 'deleted'}, status=200)
    raise Http404
