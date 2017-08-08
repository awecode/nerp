from django.template import Library

from authority_handover.numberwords import number_to_words

register = Library()


@register.filter
def nwords(number):
    return number_to_words(number)
