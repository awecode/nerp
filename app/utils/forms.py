import os
import re
from django import forms
from django.forms import Form
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404, redirect


def _slug_strip(value, separator='-'):
    """
    Cleans up a slug by removing slug separator characters that occur at the
    beginning or end of a slug.

    If an alternate separator is used, it will also replace any instances of
    the default '-' separator with the new separator.
    """
    separator = separator or ''
    if separator == '-' or not separator:
        re_sep = '-'
    else:
        re_sep = '(?:-|%s)' % re.escape(separator)
        # Remove multiple instances and if an alternate separator is provided,
    # replace the default '-' separator.
    if separator != re_sep:
        value = re.sub('%s+' % re_sep, separator, value)
        # Remove separator from the beginning and end of the slug.
    if separator:
        if separator != '-':
            re_sep = re.escape(separator)
        value = re.sub(r'^%s+|%s+$' % (re_sep, re_sep), '', value)
    return value


def unique_slugify(instance, value, slug_field_name='slug', queryset=None, slug_separator='-'):
    """
    Calculates and stores a unique slug of ``value`` for an instance.

    ``slug_field_name`` should be a string matching the name of the field to
    store the slug in (and the field to check against for uniqueness).

    ``queryset`` usually doesn't need to be explicitly provided - it'll default
    to using the ``.all()`` queryset from the model's default manager.
    """
    slug_field = instance._meta.get_field(slug_field_name)

    slug = getattr(instance, slug_field.attname)
    slug_len = slug_field.max_length

    # Sort out the initial slug, limiting its length if necessary.
    slug = slugify(value)
    if slug_len:
        slug = slug[:slug_len]
    slug = _slug_strip(slug, slug_separator)
    original_slug = slug

    # Create the queryset if one wasn't explicitly provided and exclude the
    # current instance from the queryset.
    if queryset is None:
        queryset = instance.__class__._default_manager.all()
    if instance.pk:
        queryset = queryset.exclude(pk=instance.pk)

    # Find a unique slug. If one matches, at '-2' to the end and try again
    # (then '-3', etc).
    next = 2
    while not slug or queryset.filter(**{slug_field_name: slug}):
        slug = original_slug
        end = '%s%s' % (slug_separator, next)
        if slug_len and len(slug) + len(end) > slug_len:
            slug = slug[:slug_len - len(end)]
            slug = _slug_strip(slug, slug_separator)
        slug = '%s%s' % (slug, end)
        next += 1

    setattr(instance, slug_field.attname, slug)


class ExtFileField(forms.FileField):
    """
    Same as forms.FileField, but you can specify a file extension whitelist.

    Traceback (most recent call last):
    ...
    ValidationError: [u'Not allowed filetype!']
    """

    def __init__(self, *args, **kwargs):
        ext_whitelist = kwargs.pop("ext_whitelist")
        self.ext_whitelist = [i.lower() for i in ext_whitelist]

        super(ExtFileField, self).__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        data = super(ExtFileField, self).clean(*args, **kwargs)
        if data is None:
            if self.required:
                raise forms.ValidationError("This file is required")
            else:
                return
        elif data is not False:
            filename = data.name
            ext = os.path.splitext(filename)[1]
            ext = ext.lower()
            if ext not in self.ext_whitelist:
                file_types = ", ".join([i for i in self.ext_whitelist])
                error = "Only allowed file types are: %s" % file_types
                raise forms.ValidationError(error)


class KOModelForm(forms.ModelForm):
    class EmailTypeInput(forms.widgets.TextInput):
        input_type = 'email'

    class NumberTypeInput(forms.widgets.TextInput):
        input_type = 'number'

    class TelephoneTypeInput(forms.widgets.TextInput):
        input_type = 'tel'

    class DateTypeInput(forms.widgets.DateInput):
        input_type = 'date'

    class DateTimeTypeInput(forms.widgets.DateTimeInput):
        input_type = 'datetime'

    class TimeTypeInput(forms.widgets.TimeInput):
        input_type = 'time'

    def __init__(self, *args, **kwargs):
        super(KOModelForm, self).__init__(*args, **kwargs)
        self.refine()

    def refine(self):
        for (name, field) in self.fields.items():
            widget = field.widget
            widget.attrs['data-bind'] = 'value: ' + name
            exclude_form_control = ['CheckboxInput', 'RadioSelect']
            if widget.__class__.__name__ in exclude_form_control:
                continue
            if field.required:
                field.widget.attrs['required'] = 'required'
            if 'class' in widget.attrs:
                widget.attrs['class'] += ' form-control'
            else:
                widget.attrs['class'] = 'form-control'
            if hasattr(self.Meta, 'localize'):
                if name in self.Meta.localize:
                    widget.attrs['data-bind'] += ', localize: true'
                    if 'class' in widget.attrs:
                        widget.attrs['class'] += ' localize'
                    else:
                        widget.attrs['class'] = 'localize'


class UserModelChoiceField(forms.ModelChoiceField):
    '''
    A ModelChoiceField to represent User
    select boxes in the Auto Admin
    '''

    def label_from_instance(self, obj):
        return "%s" % (obj.full_name)


def form_view(some_func):
    def inner(*args, **kwargs):
        dct = some_func(args, kwargs)
        request = (args)[0]
        id = kwargs.get('id')
        if id:
            obj = get_object_or_404(dct['model'], id=id)
            scenario = 'Update'
        else:
            obj = dct['model']()
            scenario = 'Create'
        if request.POST:
            form = dct['form'](data=request.POST, instance=obj)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.save()
                if request.is_ajax():
                    return json_from_object(obj)
                return redirect(reverse(dct['listing_url']))
        else:
            form = dct['form'](instance=obj)
        if request.is_ajax():
            base_template = 'modal.html'
        else:
            base_template = 'hr_report_base.html'
        return render(request, dct['template'], {
            'scenario': scenario,
            'form': form,
            'base_template': base_template,
        })

    return inner


class BootstrapForm(Form):
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        self.exclude = kwargs.pop('exclude', None)
        super(BootstrapForm, self).__init__(*args, **kwargs)
        if self.exclude:
            del self.fields[self.exclude]
        self.refine()

    def refine(self):
        for (i, (name, field)) in enumerate(self.fields.items()):
            widget = field.widget
            exclude_form_control = ['CheckboxInput', 'RadioSelect']
            if widget.__class__.__name__ in exclude_form_control:
                continue
            if 'class' in widget.attrs:
                widget.attrs['class'] += ' form-control'
            else:
                widget.attrs['class'] = 'form-control'
            # Auto-focus for first field of forms
            if i == 0:
                widget.attrs['autofocus'] = True


class BootstrapModelForm(BootstrapForm, forms.ModelForm):
    pass


class HTML5ModelForm(forms.ModelForm):
    required_css_class = 'required'

    class EmailTypeInput(forms.widgets.TextInput):
        input_type = 'email'

    class NumberTypeInput(forms.widgets.TextInput):
        input_type = 'number'

    class TelephoneTypeInput(forms.widgets.TextInput):
        input_type = 'tel'

    class DateTypeInput(forms.widgets.DateInput):
        input_type = 'date'

    class DateTimeTypeInput(forms.widgets.DateTimeInput):
        input_type = 'datetime'

    class TimeTypeInput(forms.widgets.TimeInput):
        input_type = 'time'

    def __init__(self, *args, **kwargs):
        self.exclude = kwargs.pop('exclude', None)
        super(HTML5ModelForm, self).__init__(*args, **kwargs)
        if self.exclude:
            del self.fields[self.exclude]
        self.refine()

    def refine(self):
        for (name, field) in self.fields.items():
            file_fields = [forms.fields.ImageField, forms.fields.FileField]
            # add HTML5 required attribute for required fields, except for file fields which already have a value
            if field.required and not (field.__class__ in file_fields and getattr(self.instance, name)):
                field.widget.attrs['required'] = 'required'

    def hide_field(self, request):
        for query in request.GET:
            if query[-3:] == '_id':
                query = query[:-3]
            self.fields[query].widget = self.fields[query].hidden_widget()
            self.fields[query].label = ''
        return self


class HTML5BootstrapModelForm(HTML5ModelForm):
    def refine(self):
        super(HTML5BootstrapModelForm, self).refine()
        for (name, field) in self.fields.items():
            widget = field.widget
            exclude_form_control = ['CheckboxInput', 'RadioSelect']
            if widget.__class__.__name__ in exclude_form_control:
                continue
            if 'class' in widget.attrs:
                widget.attrs['class'] += ' form-control'
            else:
                widget.attrs['class'] = 'form-control'
