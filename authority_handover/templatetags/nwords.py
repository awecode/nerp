from django.template import Library

from authority_handover.numberwords import number_to_words

register = Library()


@register.assignment_tag
def add(value1, value2):
    return value1 + value2


@register.filter
def nwords(number):
    return number_to_words(number)
