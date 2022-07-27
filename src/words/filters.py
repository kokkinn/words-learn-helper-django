import django_filters
from django import forms
from django_filters.widgets import BooleanWidget

from words.models import Word, GroupOfWords


def groups(request):
    if request is None:
        return GroupOfWords.objects.none()
    return request.user.groups_of_words.all()


class CustomBooleanWidget(BooleanWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.choices = (("true", 'ASC'), ("false", 'DESC'))


class WordFilter(django_filters.FilterSet):
    group = django_filters.ModelMultipleChoiceFilter(queryset=groups, widget=forms.CheckboxSelectMultiple())
    # username = django_filters.CharFilter(method='my_custom_filter')
    order_by_asc_score = django_filters.BooleanFilter(label="Order score by", method="order_by_asc_scoree",
                                                      widget=CustomBooleanWidget)

    def order_by_asc_scoree(self, queryset, name, value):
        if value:
            return queryset.order_by("score")
        else:
            return queryset.order_by("-score")

    class Meta:
        model = Word
        fields = {"score": ["lt", "gt"], "word1": ["icontains"], "word2": ["icontains"]}
