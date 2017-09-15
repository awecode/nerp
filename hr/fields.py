import datetime

from django.db.models.fields import DateField
from django.forms.fields import DateField as DateFormField
from django.core.exceptions import ValidationError

from django.forms import widgets, Media
from django.utils.safestring import mark_safe
from njango import nepdate

from app import settings
from hr.bsdate import BSDate
from hr.helpers import bs_str2tuple


class HRBSFormField(widgets.TextInput):
    def __init__(self, attrs=None):
        # class_name = get_calendar() + '-date'
        # if attrs:
        #     attrs['class'] = class_name
        # else:
        #     attrs = {'class': class_name}
        super(HRBSFormField, self).__init__(attrs)

    def _media(self):
        from hr.models import PayrollConfig
        CALENDAR = PayrollConfig.get_solo().hr_calendar
        if CALENDAR == 'BS':

            # TODO place CSS in proper path
            css = {
                'all': ('hr/njango/css/nepali.datepicker.v2.1.min.css',)
            }
            js = ('hr/njango/js/nepali.datepicker.v2.1.min.js',)
        else:
            css = {}
            js = ()

        return Media(css=css, js=js)

    def render(self, name, value, attrs=None):
        html = super(HRBSFormField, self).render(name, value, attrs)
        el_id = self.build_attrs(attrs).get('id')
        html += self.trigger_picker(el_id)
        return mark_safe(html)

    def trigger_picker(self, el_id):
        from hr.models import PayrollConfig
        CALENDAR = PayrollConfig.get_solo().hr_calendar

        if CALENDAR == 'BS':
            str = """
            <script>
                $(function(){
                    $('#%s').nepaliDatePicker({
                    onFocus: false,
                    npdMonth: true,
                    npdYear: true,
                    ndpTriggerButton: true,
                    ndpTriggerButtonText: '<span class="glyphicon glyphicon-calendar" aria-hidden="true"></span>',
                    ndpTriggerButtonClass: 'btn btn-primary btn-sm',
                    onClose: function() {
                        $(this).change(); // Forces re-validation
                    }

                    });
                });
            </script>""" % (el_id)
        else:
            str = """
            <script>
                $(function(){
                    $('#%s').datepicker({
                        format: 'yyyy-mm-dd',
                        onClose: function() {
                            $(this).change(); // Forces re-validation
                        }
                    });
                });
            </script>""" % (el_id)
        return str

    media = property(_media)


# Widgets Ends Here


class HRBSDateFormField(DateFormField):
    def __init__(self, *args, **kwargs):
        super(HRBSDateFormField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        from hr.models import PayrollConfig
        CALENDAR = PayrollConfig.get_solo().hr_calendar

        if not value:
            return value

        try:
            if CALENDAR == "AD":
                return self.strptime(value, "%Y-%m-%d")
            else:
                return BSDate(*bs_str2tuple(value))
        except:
            raise ValidationError(
                self.default_error_messages['invalid'],
                code='invalid',
                params={'value': value},
            )


class HRBSDateField(DateField):
    def from_db_value(self, value, expression, connection, context):
        from hr.models import PayrollConfig
        CALENDAR = PayrollConfig.get_solo().hr_calendar

        if CALENDAR == 'AD':
            return value
        if value is None:
            return value
        if isinstance(value, datetime.datetime):
            # TODO Timezone Awareness
            # return nepdate.string_from_tuple(nepdate.ad2bs(value.date()))
            return BSDate(*nepdate.ad2bs(value))
        if isinstance(value, datetime.date):
            # return nepdate.string_from_tuple(nepdate.ad2bs(value))
            return BSDate(*nepdate.ad2bs(value))

    def get_internal_type(self):
        return "DateField"

    def to_python(self, value):
        if not value:
            return None
        for validator in self.validators:
            validator(value)
        return value

    def get_db_prep_value(self, value, connection, prepared=False):
        from hr.models import PayrollConfig
        try:
            CALENDAR = PayrollConfig.get_solo().hr_calendar
        except:
            CALENDAR = None

        if type(value) == tuple:
            value = nepdate.string_from_tuple(value)
        value = super(HRBSDateField, self).get_db_prep_value(
            value, connection, prepared)
        if isinstance(value, datetime.date):
            return value
        if not value:
            return None

        if CALENDAR == 'AD':
            if type(value) == tuple:
                return '-'.join([str(x).zfill(2) for x in value])
            else:
                return value
        if isinstance(value, BSDate):
            return nepdate.string_from_tuple(nepdate.bs2ad(value.as_string()))
        return nepdate.string_from_tuple(nepdate.bs2ad(value))
        # return value.as_string()

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return str(value)

    def formfield(self, **kwargs):
        defaults = {
            'widget': HRBSFormField,
            'form_class': HRBSDateFormField
        }
        defaults.update(kwargs)
        # import ipdb
        # ipdb.set_trace()
        return super(DateField, self).formfield(**defaults)

    @classmethod
    def today(cls):
        from hr.models import PayrollConfig
        CALENDAR = PayrollConfig.get_solo().hr_calendar

        if CALENDAR == 'AD':
            return datetime.date.today()
        return nepdate.today_as_str()


def today():
    from hr.models import PayrollConfig
    try:
        CALENDAR = PayrollConfig.get_solo().hr_calendar
    except:
        CALENDAR = None

    if CALENDAR == 'AD':
        return datetime.date.today()
    return nepdate.today_as_str()
