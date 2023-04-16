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
    word1 = django_filters.CharFilter(lookup_expr='icontains')
    word2 = django_filters.CharFilter(lookup_expr='icontains')
    score_gt = django_filters.NumberFilter(lookup_expr='gt', field_name='score')
    score_lt = django_filters.NumberFilter(lookup_expr='lt', field_name="score")
    groups = django_filters.ModelMultipleChoiceFilter(queryset=groups, widget=forms.CheckboxSelectMultiple)
    order_by_asc_score = django_filters.BooleanFilter(label="Order score by", method="order_by_asc_scoree",
                                                      widget=CustomBooleanWidget)

    def __init__(self, data=None, queryset=None, *, request=None, prefix=None):
        super(WordFilter, self).__init__(data=data, queryset=queryset, request=request, prefix=prefix)

    def order_by_asc_scoree(self, queryset, name, value):
        if value:
            return queryset.order_by("score")
        else:
            return queryset.order_by("-score")

    class Meta:
        model = Word
        fields = []
