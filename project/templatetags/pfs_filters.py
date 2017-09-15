from django.template import Library

register = Library()


@register.filter
def against(jv, acc):
    if jv.dr == acc:
        return jv.cr
    if jv.cr == acc:
        return jv.dr


@register.filter
def is_dr(jv, acc):
    return jv.dr == acc
