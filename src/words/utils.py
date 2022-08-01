import re


def word_is_list(word):
    if len(word.split(",") or word.split(", ")) > 1:
        return True
    else:
        return False


def normalize_word(word):
    pattern = r", *"
    word = re.sub(pattern, ", ", word)
    pattern = r'[^\w, ]'
    word = re.sub(pattern, "", word)
    return word.strip(" ").strip(",").lower()


# def convert_word_to_list(word):
#     word = normalize_word(word)
#     if len(word.split(",")) > 1:
#         return word.split(",")
#     # elif len(word.split(", ")) > 1:
#     #     return word.split(", ")
#     else:
#         return list(word)
