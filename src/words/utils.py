import random
import re

from words.models import Word


def word_is_list(word):
    if len(word.split(",") or word.split(", ")) > 1:
        return True
    else:
        return False


def normalize_word(word: str):
    pattern = r", *"
    word = re.sub(pattern, ", ", word)
    # pattern = r'[^\w, ]'
    # word = re.sub(pattern, "", word)
    # pattern = r''
    # word = re.sub(pattern, "", word)
    return word.strip(" ").strip(",")


# def convert_word_to_list(word):
#     word = normalize_word(word)
#     if len(word.split(",")) > 1:
#         return word.split(",")
#     # elif len(word.split(", ")) > 1:
#     #     return word.split(", ")
#     else:
#         return list(word)

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
