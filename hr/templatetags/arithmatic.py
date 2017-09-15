from django import template

register = template.Library()


@register.assignment_tag
def add(value1, value2):
    return value1 + value2


@register.assignment_tag
def sub(value1, value2):
    return value1 - value2


@register.assignment_tag
def mul(value1, value2):
    return value1 * value2


@register.assignment_tag
def div(value1, value2):
    return value1 / value2
