from django.db import connection


def invalid(row, required_fields):
    invalid_attrs = []
    for attr in required_fields:
        # if one of the required attributes isn't received or is an empty string
        if not attr in row or row.get(attr) == "" or row.get(attr) is None:
            invalid_attrs.append(attr)
    if len(invalid_attrs) is 0:
        return False
    return invalid_attrs


def empty_to_none(o):
    if o == '':
        return None
    return o


def all_empty(row, required_fields):
    empty = True
    for attr in required_fields:
        # if one of the required attributes isn received or is not an empty string
        if attr in row and row.get(attr) != "":
            empty = False
    return empty


def save_model(model, values):
    for key, value in values.items():
        setattr(model, key, value)
    model.save()
    return model


def zero_for_none(obj):
    if obj is None or obj is '':
        return 0
    else:
        return obj


def float_zero_for_none(obj):
    if obj is None or obj is '':
        return 0
    else:
        return float(obj)


def none_for_zero(obj):
    if not obj:
        return None
    else:
        return obj


def add(*args):
    total = 0
    for arg in args:
        if arg == '':
            arg = 0
        total += float(arg)
    return total


def title_case(line):
    return ' '.join([s[0].upper() + s[1:] for s in line.split(' ')])


def model_exists_in_db(model):
    return model._meta.db_table in connection.introspection.table_names()

def merge_dicts(*dict_args):
    '''
    Given any number of dicts, shallow copy and merge into a new dict,
    precedence goes to key value pairs in latter dicts.
    '''
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result