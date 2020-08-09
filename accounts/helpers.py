from .models import LANG_CHOICES

def lang_choices_as_dict():
    lang_choices = []
    for lang in LANG_CHOICES:
        lang_choice = {
            'value': lang[0],
            'label': lang[1],
        }
        lang_choices.append(lang_choice)
    return lang_choices