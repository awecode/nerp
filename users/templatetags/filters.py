# -*- coding: utf-8 -*-

import json
from datetime import date, timedelta
import importlib

from django.core import serializers
from django.db.models.query import QuerySet
from django.template import Library, TemplateSyntaxError, Node
from django.utils.safestring import mark_safe
from django.db.models import Model
from django import template
from django.contrib.auth.models import Group
from django.utils.translation import get_language

from njango.utils import get_calendar

from app import settings
from app.utils.helpers import float_zero_for_none

from django.apps import apps
register = Library()


@register.simple_tag()
def multiply(a, b):
    if a and b:
        return a * b
    return ''


@register.simple_tag
def localize_header():
    from core.models import AppSetting

    app_setting = AppSetting.get_solo()
    value = app_setting.header_for_forms
    if not value:
        return app_setting.site_name
    lang_code = get_language()
    if lang_code == 'ne':
        value = app_setting.header_for_forms_nepali
    return value


@register.filter
def bsdate(value, arg=None):
    if type(value) in [str, unicode]:
        return value
    from django.template.defaultfilters import date

    return date(value, arg)


def handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    elif isinstance(obj, QuerySet) and not obj:
        return []
    else:
        raise TypeError, 'Object of type %s with value of %s is not JSON serializable' % (type(obj), repr(obj))


@register.filter
def jsonify(object):
    if isinstance(object, QuerySet):
        return serializers.serialize('json', object)
    if isinstance(object, Model):
        model_dict = object.__dict__
        del model_dict['_state']
        return mark_safe(json.dumps(model_dict))
    return mark_safe(json.dumps(object, default=handler))


@register.filter
def user_to_json(user):
    if hasattr(user, '_wrapped') and hasattr(user, '_setup'):
        if user._wrapped.__class__ == object:
            user._setup()
        user = user._wrapped
    user_dict = {'id': user.id, 'username': user.username}
    return mark_safe(json.dumps(user_dict))


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def if_not_none(obj):
    if obj is None:
        return ''
    return obj


@register.filter
def str_equals(value, arg):
    return str(value) == str(arg)


@register.filter
def subtract(value, arg):
    if value is None:
        value = 0
    if arg is None:
        arg = 0
    if not value:
        value = 0
    return value - arg


@register.simple_tag
def yesterday():
    today = date.today()
    yesterday = today - timedelta(days=1)
    return yesterday


@register.tag()
def ifusergroup(parser, token):
    """ Check to see if the currently logged in user belongs to one or more groups
    Requires the Django authentication contrib app and middleware.

    Usage: {% ifusergroup Admins %} ... {% endifusergroup %}, or
           {% ifusergroup Admins Clients Programmers Managers %} ... {% else %} ... {% endifusergroup %}

    """
    try:
        tokens = token.split_contents()
        groups = []
        groups += tokens[1:]
    except ValueError:
        raise template.TemplateSyntaxError("Tag 'ifusergroup' requires at least 1 argument.")

    nodelist_true = parser.parse(('else', 'endifusergroup'))
    token = parser.next_token()

    if token.contents == 'else':
        nodelist_false = parser.parse(('endifusergroup',))
        parser.delete_first_token()
    else:
        nodelist_false = template.NodeList()

    return GroupCheckNode(groups, nodelist_true, nodelist_false)


class GroupCheckNode(template.Node):
    def __init__(self, groups, nodelist_true, nodelist_false):
        self.groups = groups
        self.nodelist_true = nodelist_true
        self.nodelist_false = nodelist_false

    def render(self, context):
        user = template.resolve_variable('user', context)

        if not user.is_authenticated():
            return self.nodelist_false.render(context)

        allowed = False
        for checkgroup in self.groups:

            if checkgroup.startswith('"') and checkgroup.endswith('"'):
                checkgroup = checkgroup[1:-1]

            if checkgroup.startswith("'") and checkgroup.endswith("'"):
                checkgroup = checkgroup[1:-1]

            try:
                group = Group.objects.get(name=checkgroup)
            except Group.DoesNotExist:
                break

            if group in user.groups.all():
                allowed = True
                break

        if allowed:
            return self.nodelist_true.render(context)
        else:
            return self.nodelist_false.render(context)


@register.filter
def setting(path):
    to_import = '.'.join(path.split('.')[:-2])
    imported = importlib.import_module(to_import)
    group_name = path.split('.')[-2:-1][0]
    group = getattr(imported, group_name)
    attr_name = path.split('.')[-1]
    val = getattr(group, attr_name)
    return val


@register.tag
def ifappexists(parser, token):
    """ Conditional Django template tag to check if one or more apps exist.

    Usage: {% ifappexists tag %} ... {% endifappexists %}, or
           {% ifappexists tag inventory %} ... {% else %} ... {% endifappexists %}

    """
    try:
        tokens = token.split_contents()
        apps = []
        apps += tokens[1:]
    except ValueError:
        raise template.TemplateSyntaxError("Tag 'ifappexists' requires at least 1 argument.")

    nodelist_true = parser.parse(('else', 'endifappexists'))
    token = parser.next_token()

    if token.contents == 'else':
        nodelist_false = parser.parse(('endifappexists',))
        parser.delete_first_token()
    else:
        nodelist_false = template.NodeList()

    return AppCheckNode(apps, nodelist_true, nodelist_false)


class AppCheckNode(template.Node):
    def __init__(self, apps, nodelist_true, nodelist_false):
        self.apps = apps
        self.nodelist_true = nodelist_true
        self.nodelist_false = nodelist_false

    def render(self, context):
        allowed = False
        for app in self.apps:

            if app.startswith('"') and app.endswith('"'):
                app = app[1:-1]

            if app.startswith("'") and app.endswith("'"):
                app = app[1:-1]

            if app in settings.INSTALLED_APPS:
                allowed = True
            else:
                break

        if allowed:
            return self.nodelist_true.render(context)
        else:
            return self.nodelist_false.render(context)


@register.filter
def linebreaks(obj):
    return mark_safe(obj.replace("\n", "<br>"))


@register.filter
def linkify(obj):
    # import pdb
    #
    # pdb.set_trace()
    if obj:
        return mark_safe('<a href="' + obj.get_absolute_url() + '">' + unicode(obj) + '</a>')


@register.filter
def is_demand(obj):
    if obj.__class__.__name__ == 'DemandRow':
        return True
    return False


@register.filter
def get_class(value):
    return value.__class__.__name__


@register.filter
def localize(text):
    lang_code = get_language()
    if lang_code == 'ne':
        text = str(text)
        dic = {
            '०': '0',
            '१': '1',
            '२': '2',
            '३': '3',
            '४': '4',
            '५': '5',
            '६': '6',
            '७': '7',
            '८': '8',
            '९': '9'
        }
        res = dict((v, k) for k, v in dic.iteritems())
        for i, j in res.iteritems():
            text = text.replace(i, j)
    return text


@register.filter
def debug(value):
    import pdb

    pdb.set_trace()


@register.filter
def mailto(email, linktext=None):
    if not email:
        return ''
    if linktext is None: linktext = email
    return mark_safe('<a href="mailto:%s">%s</a>' % (email, linktext))


@register.filter
def to_class_name(value):
    return value.__class__.__name__


@register.assignment_tag
def get_fiscal_years():
    from core.models import FiscalYear

    return FiscalYear.objects.all()


@register.filter
def fiscal_year(year):
    year = int(year)
    calendar = get_calendar()
    if calendar == 'ad':
        year -= 57
    return str(year) + '/' + str(year - 1999)


@register.assignment_tag
def get_previous(loop, lst):
    return lst[loop['counter'] - 2]


@register.assignment_tag
def remaining_total_cost_price(row, counter, data):
    if row.get('remaining_total_cost_price'):
        return float(row.get('remaining_total_cost_price'))
    if counter == 0:
        return float_zero_for_none(row.get('income_total')) - float_zero_for_none(row.get('expense_total'))
    previous_row = data[counter - 1]
    return float_zero_for_none(row.get('income_total')) - float_zero_for_none(
        row.get('expense_total')) + remaining_total_cost_price(
        previous_row, counter - 1, data)


@register.filter
def dr_or_cr(val):
    if val < 0:
        return str(val * -1) + ' (Cr)'
    else:
        return str(val) + ' (Dr)'


@register.filter
def get_particulars(entry, account):
    lst = []
    source = entry.content_type.get_object_for_this_type(id=entry.object_id)
    for row in source.journal_voucher.rows.all():
        if row.account is not None and not row.account == account:
            lst.append('<a href="' + '/ledger/' + str(row.account.id) + '/#' + str(entry.id) + '">' + str(
                row.account) + '</a>')
    return ', '.join(lst)


@register.filter
def remove_account(transactions, account):
    return [transaction for transaction in transactions if
            transaction.account.id != account.id]


@register.filter
def refine_voucher_type(the_type):
    if the_type[-4:] == ' row':
        the_type = the_type[:-3]
    if the_type[-11:] == ' particular':
        the_type = the_type[:-10]
    return the_type.title()


@register.filter
def to_char(value):
    return unichr(value + 64)


@register.tag
def get_obj(parser, token):
    bits = token.split_contents()
    if len(bits) is 4:
        return ListObject(bits[1], bits[3])
    else:
        raise TemplateSyntaxError, "invalid number of arguments"

class ListObject(Node):
    def __init__(self, model, varname):
        self.model = apps.get_model(*model.split('.'))
        self.varname = varname

    def render(self, context):
        context[self.varname] = self.model._default_manager.all()
        return ''
