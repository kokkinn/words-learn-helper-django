import json
import random
import re
from django.http import JsonResponse

from words.models import Word


def word_is_list(word):
    if len(word.split(",") or word.split(", ")) > 1:
        return True
    else:
        return False


def normalize_word(word: str):
    pattern = r", *"
    word = re.sub(pattern, ", ", word)
    return word.strip(" ").strip(",")


def word_with_min_score_from_id_array(id_aray: list):
    random.shuffle(id_aray)
    min_score = Word.objects.filter().order_by('score').last().score
    list_word_id_with_min_score = []
    for id_ in id_aray:
        if Word.objects.get(id=id_).score < min_score:
            min_score = Word.objects.get(id=id_).score
            list_word_id_with_min_score.append(Word.objects.get(id=id_).id)
        elif Word.objects.get(id=id_).score == min_score:
            list_word_id_with_min_score.append(id_)
    return Word.objects.get(id=random.choice(list_word_id_with_min_score))


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def json_response_form_errors(form) -> JsonResponse:
    """
    Returns JsonResponse object filled with form errors.

    "errors_list" key of response is a list of errors as strings.

    "status" key of response is "form_invalid" stringf.

    :param form: django filled form
    :return: JsonResponse object
    """

    errors_list = []
    if form.errors:
        for field in form:
            for error in field.errors:
                errors_list.append(error)
    return JsonResponse({"errors_list": json.dumps(errors_list), "status": json.dumps("form_invalid")},
                        status=200)
