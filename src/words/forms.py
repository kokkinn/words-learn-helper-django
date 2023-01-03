from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.forms import ModelForm, ModelMultipleChoiceField, ChoiceField, ModelChoiceField
from .models import Word, GroupOfWords, Result
from django import forms

from .utils import word_is_list, normalize_word


class WordCUForm(ModelForm):
    word1 = forms.CharField(validators=[MinLengthValidator(1, message='Please, fill the field'),
                                        MaxLengthValidator(50,
                                                           message='Word should not be longer than %(limit_value)d symbols')
                                        ],
                            widget=forms.TextInput())
    word2 = forms.CharField(validators=[MinLengthValidator(1, message='Please, fill the field'),
                                        MaxLengthValidator(50,
                                                           message='Translation should not be longer than %(limit_value)d symbols')],
                            widget=forms.TextInput())
    groups = ModelMultipleChoiceField(queryset=None,
                                      widget=forms.CheckboxSelectMultiple,
                                      required=False)  # we defined a qs in init method

    class Meta:
        model = Word
        fields = ['word1', 'word2', 'groups']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')  # we pop it because it is not expected in constructor
        super(WordCUForm, self).__init__(*args, **kwargs)
        self.fields['groups'].queryset = GroupOfWords.objects.filter(user=self.request.user).exclude(
            id=self.request.user.general_group.id)

    def clean(self):
        cleaned_data = super().clean()
        if 'word1' in cleaned_data.keys() and 'word2' in cleaned_data.keys():  # if field is not validated, it won't
            cleaned_data["word1"] = normalize_word(cleaned_data["word1"])  # in a cleaned data dictionary
            cleaned_data["word2"] = normalize_word(cleaned_data["word2"])
        return self.cleaned_data


class GroupCUForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(GroupCUForm, self).__init__(*args, **kwargs)
        self.fields['words'].queryset = Word.objects.filter(user=self.request.user)

    class Meta:
        model = GroupOfWords
        fields = ("name", "description", 'words')
        widgets = {'words': forms.CheckboxSelectMultiple}


class GroupChoiceForm(forms.Form):
    def __init__(self, user, *args, **kwargs, ):
        super(GroupChoiceForm, self).__init__(*args, **kwargs)
        self.user = user
        groups_qs = GroupOfWords.objects.filter(user=self.user)
        for group in groups_qs:
            if not qs_not_empty(group):
                groups_qs = groups_qs.exclude(id=group.id)
        self.fields['groups'].queryset = groups_qs

    groups = forms.ModelChoiceField(queryset=None)


class TestInputForm(forms.Form):
    input_word = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Your input...'}))


def qs_not_empty(query_set):
    return False if query_set.words.count() == 0 else True


class TestParametersForm(forms.ModelForm):
    groups = forms.ModelMultipleChoiceField(queryset=None, widget=forms.CheckboxSelectMultiple, required=False)

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        super(TestParametersForm, self).__init__(*args, **kwargs)
        # print(request.user.groups_of_words.all() | request.user.general_group)
        self.fields['groups'].queryset = request.user.groups_of_words.all()

    class Meta:
        model = Result
        fields = ['groups', 'duration', 'do_with_incorrect', 'word2examine_number', 'which_goes_first', 'scoring_type']
    # def __init__(self, user, *args, **kwargs, ):
    #     super(TestParametersForm, self).__init__(*args, **kwargs)
    #     self.user = user
    #     groups_qs = GroupOfWords.objects.filter(user=self.user)
    #     for group in groups_qs:
    #         if not qs_not_empty(group):
    #             groups_qs = groups_qs.exclude(id=group.id)
    #     self.fields['groups'].queryset = groups_qs

    # help_text_groups = "A 'Group', all Pairs of which will be included in the test."
    # help_text_durations = "'Loop' for infinite test for Pairs of a group. If 'Finite' is chosen, test will end, after all answers will be submitted, result will be created."
    # help_text_type = "'Ranked' for answer will change the score, If 'Unranked', score won't be affected."
    # help_text_test_for_translation_of = "'A user's choice defines translation of what word will be asked."
    # help_text_do_with_incorrect = "If 'repeat' is chosen, test won't end until all answers are answered correctly."
    # help_text_lower_score_first = "Pick 'Pairs with lower are asked firstly' if ypu want to test Pairs with lower score"
