from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect

from words.models import Word, GroupOfWords

from words.forms import GroupCUForm
from django.http import HttpResponseRedirect, Http404

from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import FormView, DeleteView


class GroupsListView(LoginRequiredMixin, ListView):
    template_name = "words/group_list.html"
    model = GroupOfWords
    context_object_name = 'groups'

    def get_queryset(self):
        super(GroupsListView, self).get_queryset()
        print(self.request.user.groups_of_words.all())
        return self.request.user.groups_of_words.all().exclude(id=self.request.user.general_group.id)

    def post(self, request):
        checks = request.POST.getlist("checks[]")
        for idi in checks:
            group = GroupOfWords.objects.get(id=idi)
            if group.name == "General":
                return HttpResponseRedirect(reverse_lazy("words:home"))
            group.delete()
            # messages.success(self.request, f"Group '{group.name}' deleted")
        return redirect(reverse_lazy("words:groups_list"))


class GroupCreateView(LoginRequiredMixin, FormView):
    template_name = "words/group_CU_form.html"
    form_class = GroupCUForm
    success_url = reverse_lazy("words:groups_list")

    def form_valid(self, form):
        super().form_valid(self)
        group_obj = form.instance
        words = form.cleaned_data['words']
        group_obj.user = self.request.user
        group_obj.save()
        for word in words:
            group_obj.words.add(word)
        group_obj.save()
        # messages.success(self.request, f"Group '{form.instance.name}' created")
        return HttpResponseRedirect(reverse_lazy("words:groups_list"))

    def get_context_data(self, **kwargs):
        context = super(GroupCreateView, self).get_context_data()
        context["type"] = "create"
        no_words = None
        if len(self.request.user.words.all()) == 0:
            no_words = True
        context['no_words'] = no_words
        return context

    def get_form_kwargs(self):
        kwargs = super(GroupCreateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class GroupUpdateView(LoginRequiredMixin, FormView):
    template_name = "words/group_CU_form.html"
    form_class = GroupCUForm
    success_url = reverse_lazy("words:groups_list")
    pk_url_kwarg = "uuid"

    def get(self, request, *args, **kwargs):
        try:
            GroupOfWords.objects.get(user=self.request.user, id=self.kwargs["uuid"])
        except Word.DoesNotExist:
            raise Http404
        uuid = self.kwargs.get('uuid')
        group_obj = GroupOfWords.objects.get(id=uuid)
        if group_obj.name == self.request.user.general_group.name:
            return HttpResponseRedirect(reverse_lazy("words:home"))
        return super().get(self, request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(GroupUpdateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_initial(self):
        initial = super().get_initial()
        uuid = self.kwargs.get('uuid')
        group_obj = GroupOfWords.objects.get(id=uuid)
        initial['words'] = group_obj.words.all()
        initial["name"] = group_obj.name
        initial["description"] = group_obj.description
        return initial

    def form_valid(self, form):
        super().form_valid(self)
        words = form.cleaned_data['words']
        uuid = self.kwargs.get('uuid')
        group_obj = GroupOfWords.objects.get(id=uuid)
        group_obj.words.clear()
        for word in words:
            group_obj.words.add(word)
        group_obj.description = form.cleaned_data["description"]
        group_obj.name = form.cleaned_data["name"]
        group_obj.save()
        # messages.success(self.request, f"Group '{form.instance.name}' updated")

        return HttpResponseRedirect(reverse_lazy("words:groups_list"))

    def get_context_data(self, **kwargs):
        context = super(GroupUpdateView, self).get_context_data()
        context["type"] = "update"
        no_words = False
        if len(self.request.user.words.all()) == 0:
            no_words = True
        context['no_words'] = no_words
        return context


class WordsInGroupListView(ListView, LoginRequiredMixin):
    model = Word
    context_object_name = "words"
    pk_url_kwarg = 'uuid'
    template_name = 'words/group_single.html'

    def get_queryset(self):
        super(WordsInGroupListView, self).get_queryset()
        uuid = self.kwargs.get("uuid")
        return GroupOfWords.objects.get(id=uuid).words.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        uuid = self.kwargs.get("uuid")
        context["group_obj"] = GroupOfWords.objects.get(id=uuid)
        return context

    # def get_template_names(self):
    #     super().get_template_names()
    #     if not self.request.user.words.all():
    #         return ["words/no_words.html"]
    #     else:
    #         return ["words/group_single.html"]


class GroupDeleteView(DeleteView):
    model = GroupOfWords
    pk_url_kwarg = 'uuid'
    success_url = reverse_lazy('words:groups_list')
