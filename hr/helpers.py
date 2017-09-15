from __future__ import division
from datetime import date

import six
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import AccessMixin
from django.core.exceptions import ImproperlyConfigured

from bsdate import BSDate, month
from njango.nepdate import bs, bs2ad, ad2bs
from calendar import monthrange as mr
from django.utils.translation import ugettext_lazy as _

from users.templatetags.filters import localize


def get_y_m_tuple_list(from_date, to_date):
    return_list = []
    while from_date <= to_date:
        return_list.append((from_date.year, from_date.month))
        if from_date.month < 12:
            if type(from_date) == date:
                from_date = date(
                    from_date.year,
                    from_date.month + 1,
                    from_date.day
                )
            else:
                from_date = BSDate(
                    from_date.year,
                    from_date.month + 1,
                    from_date.day
                )
        else:
            if type(from_date) == date:
                from_date = date(
                    from_date.year + 1,
                    1,
                    from_date.day
                )
            else:
                from_date = BSDate(
                    from_date.year + 1,
                    1,
                    from_date.day
                )
    return return_list

def get_y_m_in_words(from_date, to_date):
    list_in_words = ['%s-%s' % (localize(tup[0]), month[tup[1]]) for tup in get_y_m_tuple_list(from_date, to_date)]
    return (' / ').join(list_in_words)


def month_cnt_inrange(month, frm, to):
    cnt = 0
    if month == frm.month == to.month:
        delta_days = (to - frm).days
        if isinstance(frm, date):
            month_total_days = mr(frm.year, frm.month)[1]
        else:
            month_total_days = bs[frm.year][frm.month - 1]
        cnt += delta_days / month_total_days
    else:
        for y, m in get_y_m_tuple_list(frm, to):
            if month == m:
                cnt += 1
    return cnt


def are_side_months(from_date, to_date):
    if from_date.year == to_date.year and to_date.month - from_date.month == 1:
        return True
    elif to_date.year - from_date.year == 1 and from_date.month - to_date.month == 11:
        return True
    else:
        return False


def bs_str2tuple(date_string):
    as_list = date_string.split('-')
    date_tuple = (
        int(as_list[0]),
        int(as_list[1]),
        int(as_list[2])
    )
    # If possible varify this
    return date_tuple


def str2BSDate(date_string):
    date_tuple = bs_str2tuple(date_string)
    return BSDate(*date_tuple)


def get_account_id(employee_object, account_type):
    from hr.models import EmployeeAccount
    return EmployeeAccount.objects.get(
        employee=employee_object,
        other_account_type=account_type
    ).account.id


def delta_month_date(p_from, p_to):
    y_m_tuple = get_y_m_tuple_list(p_from, p_to)
    total_month = len(y_m_tuple)
    total_work_day = 0
    if isinstance(p_from, date):
        if type(p_from) == type(p_to):
            for mon in y_m_tuple:
                total_work_day += mr(*mon)[1]
    else:
        if type(p_from) == type(p_to):
            for mon in y_m_tuple:
                total_work_day += bs[mon[0]][mon[1] - 1]
                # total_work_day += mr(*mon)[1]
    return (total_month, total_work_day)


def delta_month_date_impure(p_from, p_to):
    if type(p_from) == type(p_to):
        if p_from.year == p_to.year and p_from.month == p_to.month:
            total_days = (p_to - p_from).days + 1
            if isinstance(p_from, date):
                pure_month_days = mr(p_from.year, p_from.month)[1]
            else:
                pure_month_days = bs[p_from.year][p_from.month - 1]
            total_month = total_days / pure_month_days

        elif are_side_months(p_from, p_to):
            pure_month_days = 0

            if isinstance(p_from, date):
                lhs_month = date(p_from.year, p_from.month, 1)
                rhs_month = date(p_to.year, p_to.month, 1)
                lhs_month_work_days = (rhs_month - p_from).days
                rhs_month_work_days = (p_to - rhs_month).days + 1

                lhs_month_days = mr(lhs_month.year, lhs_month.month)[1]
                rhs_month_days = mr(rhs_month.year, rhs_month.month)[1]

            else:
                lhs_month = BSDate(p_from.year, p_from.month, 1)
                rhs_month = BSDate(p_to.year, p_to.month, 1)
                lhs_month_work_days = (rhs_month - p_from).days
                rhs_month_work_days = (p_to - rhs_month).days + 1

                lhs_month_days = bs[lhs_month.year][lhs_month.month - 1]
                rhs_month_days = bs[rhs_month.year][rhs_month.month - 1]
            total_month = (lhs_month_work_days / lhs_month_days) + (rhs_month_work_days / rhs_month_days)
            total_days = lhs_month_work_days + rhs_month_work_days
        else:
            if isinstance(p_from, date):
                if p_from.month == 12:
                    p_from_m = date(p_from.year + 1, 1, 1)
                else:
                    p_from_m = date(p_from.year, p_from.month + 1, 1)
                if p_to.month == 1:
                    p_to_m = date(p_to.year - 1, 12, 1)
                else:
                    p_to_m = date(p_to.year, p_to.month - 1, 1)
                lhs_month = date(p_from.year, p_from.month, 1)
                rhs_month = date(p_to.year, p_to.month, 1)
                lhs_month_work_days = (p_from_m - p_from).days
                rhs_month_work_days = (p_to - p_to_m).days + 1

                lhs_month_days = mr(lhs_month.year, lhs_month.month)[1]
                rhs_month_days = mr(rhs_month.year, rhs_month.month)[1]

            else:
                if p_from.month == 12:
                    p_from_m = BSDate(p_from.year + 1, 1, 1)
                else:
                    p_from_m = BSDate(p_from.year, p_from.month + 1, 1)
                if p_to.month == 1:
                    p_to_m = BSDate(p_to.year - 1, 12, 1)
                else:
                    p_to_m = BSDate(p_to.year, p_to.month - 1, 1)
                lhs_month = BSDate(p_from.year, p_from.month, 1)
                rhs_month = BSDate(p_to.year, p_to.month, 1)
                lhs_month_work_days = (p_from_m - p_from).days
                rhs_month_work_days = (p_to - p_to_m).days + 1

                lhs_month_days = bs[lhs_month.year][lhs_month.month - 1]
                rhs_month_days = bs[rhs_month.year][rhs_month.month - 1]

            y_m_tuple = get_y_m_tuple_list(p_from_m, p_to_m)
            total_month = len(y_m_tuple) + (lhs_month_work_days / lhs_month_days) + (
                rhs_month_work_days / rhs_month_days)
            total_days = (p_to - p_from).days + 1
    return (total_month, total_days)


def bsdate2str(date):
    li = [str(x) for x in date.date_tuple()]
    return '-'.join(li)


# This could be of 4 line haha bad one
def inc_1_day(in_date):
    if isinstance(in_date, date):
        month_days = mr(in_date.year, in_date.month)[1]
        if in_date.month == 12 and in_date.day == month_days:
            r_date = date(in_date.year + 1, 1, 1)
        elif in_date.month < 12 and in_date.day == month_days:
            r_date = date(in_date.year, in_date.month + 1, 1)
        else:
            r_date = date(in_date.year, in_date.month, in_date.day + 1)
    else:
        month_days = bs[in_date.year][in_date.month - 1]
        if in_date.month == 12 and in_date.day == month_days:
            r_date = BSDate(in_date.year + 1, 1, 1)
        elif in_date.month < 12 and in_date.day == month_days:
            r_date = BSDate(in_date.year, in_date.month + 1, 1)
        else:
            r_date = BSDate(in_date.year, in_date.month, in_date.day + 1)
    return r_date


def drc_1_day(in_date):
    if isinstance(in_date, date):
        # month_days = mr(in_date.year, in_date.month)[1]
        if in_date.month == 1 and in_date.day == 1:
            m_d = mr(in_date.year - 1, 12)[1]
            r_date = date(in_date.year - 1, 12, m_d)
        elif in_date.month > 1 and in_date.day == 1:
            m_d1 = mr(in_date.year, in_date.month - 1)[1]
            r_date = date(in_date.year, in_date.month - 1, m_d1)
        else:
            r_date = date(in_date.year, in_date.month, in_date.day - 1)
    else:
        if in_date.month == 1 and in_date.day == 1:
            # m_d = mr(in_date.year - 1, in_date.month)[1]
            m_d = bs[in_date.year - 1][12 - 1]
            r_date = BSDate(in_date.year - 1, 12, m_d)
        elif in_date.month > 1 and in_date.day == 1:
            # m_d1 = mr(in_date.year, in_date.month - 1)[1]
            m_d1 = bs[in_date.year][in_date.month - 2]
            r_date = BSDate(in_date.year, in_date.month - 1, m_d1)
        else:
            r_date = BSDate(in_date.year, in_date.month, in_date.day - 1)
    return r_date


def inc_date_by_days(in_date, inc):
    for c in range(0, inc):
        r_date = inc_1_day(in_date)
    return r_date


def drc_date_by_days(in_date, drc):
    for c in range(0, drc):
        r_date = drc_1_day(in_date)
    return r_date


def employee_last_payment_record(employee):
    from hr.models import PaymentRecord
    emp_record = PaymentRecord.objects.filter(paid_employee=employee)
    pr_last_date = None
    if emp_record:
        emp_record = sorted(
            emp_record,
            key=lambda pr: pr.paid_to_date,
            reverse=True
        )
        pr_last_date = emp_record[0].paid_to_date
    if pr_last_date:
        return pr_last_date
    else:
        return None


def emp_salary_eligibility(emp, p_from, p_to):
    error_msg = None
    never_paid = None
    emp_last_record = employee_last_payment_record(emp)

    if emp_last_record:
        last_paid = emp_last_record
    else:
        last_paid = drc_1_day(emp.scale_start_date)
        never_paid = True
    if type(last_paid) != type(p_from):
        raise TypeError('Internal and external setting mismatch')
    if p_from <= last_paid:
        if isinstance(p_from, date):
            if never_paid:
                error_msg = 'Employee has not worked yet for %s. Appointed on %s' % (
                    '{:%Y-%m-%d}'.format(p_from), '{:%Y-%m-%d}'.format(emp.appoint_date))
            else:
                error_msg = 'Already paid for/upto date %s. Last paid upto %s' % (
                    '{:%Y-%m-%d}'.format(p_from), '{:%Y-%m-%d}'.format(last_paid))
        else:
            if never_paid:
                error_msg = 'Employee has not worked yet for %s. Appointed on %s' % (
                    bsdate2str(p_from), emp.scale_start_date)
            else:
                error_msg = 'Already paid for/upto date %s. Last paid upto %s' % (
                    bsdate2str(p_from), bsdate2str(last_paid))
    elif p_from > inc_1_day(last_paid):
        if isinstance(p_from, date):
            error_msg = 'Missed payment from %s to %s' % (
                '{:%Y/%m/%d}'.format(inc_1_day(last_paid)), '{:%Y-%m-%d}'.format(drc_1_day(p_from)))
        else:
            error_msg = 'Missed payment from %s to %s' % (
                bsdate2str(inc_1_day(last_paid)), bsdate2str(drc_1_day(p_from)))
    if error_msg:
        return False, error_msg
    else:
        return True, None


def emp_salary_eligibility_on_edit(fromdate_request, todate_request, employee, edit_row):
    # import ipdb
    # ipdb.set_trace()
    error_msg = None
    fromdate_saved = edit_row.paid_from_date
    # if not isinstance(fromdate_saved, date):
    #     fromdate_saved = BSDate(*(bs_str2tuple(fromdate_saved)))
    todate_saved = edit_row.paid_to_date
    # if not isinstance(todate_saved, date):
    #     todate_saved = BSDate(*(bs_str2tuple(todate_saved)))


    # find this employee last record
    last_payment_record = employee_last_payment_record(employee)
    # fromdate_last = last_payment_record.paid_from_date
    # if not isinstance(fromdate_last, date):
    #     fromdate_last = BSDate(*(bs_str2tuple(fromdate_last)))
    # todate_last = last_payment_record.paid_to_date
    # if not isinstance(todate_last, date):
    #     todate_last = BSDate(*(bs_str2tuple(todate_last)))

    # Calculate errors from logical operations
    if fromdate_request < fromdate_saved:
        error_msg = 'Overlapped with previous entries'
    # elif last_payment_record != edit_row:
    #     if todate_request > todate_saved:
    #         error_msg = 'Overlapped with next entry'

    if error_msg:
        return False, error_msg
    else:
        return True, None


def fiscal_year_by_date(f_date):
    fiscal_year_range = None
    is_ad = False
    if isinstance(f_date, date):
        f_date = BSDate(*ad2bs(f_date))
        is_ad = True

    possible_fiscal_years = (
        (
            BSDate(f_date.year - 1, 4, 1),
            BSDate(f_date.year, 3, bs[f_date.year][2]),
        ),
        (
            BSDate(f_date.year, 4, 1),
            BSDate(f_date.year + 1, 3, bs[f_date.year + 1][2]),
        ),
    )
    for d_range in possible_fiscal_years:
        if f_date >= d_range[0] and f_date <= d_range[1]:
            fiscal_year_range = d_range

    if is_ad:
        return [date(*bs2ad(*d.date_tuple())) for d in fiscal_year_range]
    else:
        return fiscal_year_range


# In date range fiscal years, total years in that fiscal year and worked days
def fiscal_year_data(d_from, d_to):
    result = []
    # if fiscal_year_by_date(d_from) == fiscal_year_by_date(d_to):
    # result.append({
    #     'f_y': fiscal_year_by_date(d_from),
    # })
    f_year = fiscal_year_by_date(d_to)
    to_date_year = d_to.year
    to_date = d_to
    while f_year != fiscal_year_by_date(d_from):
        f_year = fiscal_year_by_date(to_date)
        result.append(
            {'f_y': f_year}
        )
        to_date_year -= 1
        if isinstance(to_date, date):
            month_total_days = mr(to_date_year, d_to.month)[1]
            to_date = date(to_date_year, d_to.month, month_total_days)
        else:
            month_total_days = bs[to_date_year][d_to.month - 1]
            to_date = BSDate(to_date_year, d_to.month, month_total_days)

    if len(result) == 0:
        result.append({
            'f_y': fiscal_year_by_date(d_from),
        })
        result[0]['worked_days'] = (d_to - d_from).days + 1
        result[0]['year_days'] = (result[0]['f_y'][1] - result[0]['f_y'][0]).days + 1
    else:
        for item in result:
            if item == result[-1]:
                item['worked_days'] = (item['f_y'][1] - d_from).days + 1
                item['year_days'] = (item['f_y'][1] - item['f_y'][0]).days + 1
            elif item == result[0]:
                item['worked_days'] = (d_to - item['f_y'][0]).days + 1
                item['year_days'] = (item['f_y'][1] - item['f_y'][0]).days + 1
            else:
                item['worked_days'] = (item['f_y'][1] - item['f_y'][0]).days + 1
                item['year_days'] = (item['f_y'][1] - item['f_y'][0]).days + 1
    return result


def empty_to_none(o):
    if o == '':
        return None
    return o


def empty_to_zero(o):
    if o == '' or o == None:
        return 0
    return o


def zero_for_none(obj):
    if obj is None:
        return 0
    else:
        return obj


def none_for_zero(obj):
    if not obj:
        return None
    else:
        return obj


class ValiditySlot(object):
    def __init__(self, from_date=None, to_date=None, validity_id=None):
        if from_date:
            self.check_for_valid_date(from_date)

        if to_date:
            self.check_for_valid_date(to_date)

        self.from_date = from_date
        self.to_date = to_date
        self.validity_id = validity_id

    def set_from_date(self, from_date):
        self.check_for_valid_date(from_date)
        self.from_date = from_date

    def set_to_date(self, to_date):
        self.check_for_valid_date(to_date)
        self.to_date = to_date

    def set_validity_id(self, validity_id):
        self.validity_id = validity_id

    def check_for_valid_date(self, in_date):
        if isinstance(in_date, date) or isinstance(in_date, BSDate):
            return True
        else:
            raise ValueError('Date must be either datetime.date or BSDate type')

    def __repr__(self):
        return 'ValiditySlot: ' + str(self.from_date) + " to " + str(self.to_date)

    def __str__(self):
        return 'ValiditySlot: ' + str(self.from_date) + " to " + str(self.to_date)


# This function get in_date belonging validity id
def get_validity_id(cls, in_date):
    return_id = None
    existing_validity = sorted(
        cls.objects.all(), key=lambda v: v.valid_from
    )
    for i, validity in enumerate(existing_validity):
        if type(in_date) == type(validity.valid_from):
            if in_date >= validity.valid_from:
                try:
                    if in_date < existing_validity[i + 1].valid_from:
                        return_id = validity.id
                        break
                except IndexError:
                    return_id = validity.id
            else:
                raise IOError('Input date does not falls on any validity')
        else:
            raise TypeError(' input date must be of calendar type (datetime.date for "AD" and BSDate for "BS")')
    if not return_id:
        raise IOError("No %s's present" % cls)
    return return_id


def get_validity_slots(cls, from_date, to_date, **kwargs):
    validity_slots = []

    if isinstance(from_date, date):
        in_between_validities = cls.objects.filter(valid_from__gte=from_date).filter(valid_from__lte=to_date)
    else:
        in_between_validities = cls.objects.filter(valid_from__gte=from_date.as_ad()).filter(
            valid_from__lte=to_date.as_ad())

    if not in_between_validities:
        try:
            validity_slots.append(
                ValiditySlot(from_date, to_date, get_validity_id(cls, from_date))
            )
        except IOError:
            raise IOError('Given range start date is less than latest valid from date. Or validity not present.')
    else:
        date_pointer = from_date
        for validity in sorted(in_between_validities, key=lambda v: v.valid_from):
            if date_pointer < validity.valid_from:
                try:
                    validity_slots.append(
                        ValiditySlot(date_pointer, drc_1_day(validity.valid_from), get_validity_id(cls, date_pointer))
                    )
                except IOError:
                    raise IOError('Given range start date is less than latest valid from date.')
                date_pointer = validity.valid_from

        if date_pointer <= to_date:
            try:
                validity_slots.append(
                    ValiditySlot(date_pointer, to_date, get_validity_id(cls, date_pointer))
                )
            except IOError:
                raise IOError('Given range start date is less than latest valid from date.')
    return validity_slots


def is_required_data_present(employee, from_date, to_date):
    from hr.models import GradeScaleValidity, EmployeeGradeScale
    errors = []
    try:
        grade_scale_validity_slots = get_validity_slots(GradeScaleValidity, from_date, to_date)
        for slot in grade_scale_validity_slots:
            gs_data = EmployeeGradeScale.objects.filter(
                grade=employee.designation.grade,
                validity_id=slot.validity_id
            )
            if not gs_data:
                validity = GradeScaleValidity.objects.get(id=slot.validity_id)
                errors.append('This employee grade has no  grade scale for: %s.[%s]' % (str(slot), validity))
    except IOError:
        raise

    if errors:
        return False, errors
    else:
        return True, None


def user_is_branch_accountant(user):
    try:
        return True if user.payroll_accountant else False
    except:
        return False


class GroupRequiredMixin(AccessMixin):
    group_required = None
    permission_denied_message = 'Only Accountant can access this page.'

    def get_group_required(self):
        if self.group_required is None or (
                not isinstance(self.group_required,
                               (list, tuple) + six.string_types)
        ):
            raise ImproperlyConfigured(
                '{0} requires the "group_required" attribute to be set and be '
                'one of the following types: string, unicode, list or '
                'tuple'.format(self.__class__.__name__))
        if not isinstance(self.group_required, (list, tuple)):
            self.group_required = (self.group_required,)
        return self.group_required

    def check_group_required(self, request, *group_names):
        """Requires user membership in at least one of the groups passed in."""

        def in_groups(u, request):
            if u.is_authenticated():
                if bool(u.groups.filter(name__in=group_names)) | u.is_superuser():
                    return True
                if bool(u.groups.filter(name__in=group_names)):
                    return True
            return self.handle_no_permission()

        return user_passes_test(in_groups)

    def dispatch(self, request, *args, **kwargs):
        has_required_group = self.check_group_required(request, self.group_required)
        if has_required_group:
            return super(GroupRequiredMixin, self).dispatch(
                request, *args, **kwargs)


class IsBranchAccountantMixin(AccessMixin):
    def user_is_branch_accountant(self, user):
        try:
            return True if user.payroll_accountant else self.handle_no_permission()
        except:
            return self.handle_no_permission()

    def dispatch(self, request, *args, **kwargs):
        is_branch_accountant = self.user_is_branch_accountant(request.user)
        if is_branch_accountant:
            return super(IsBranchAccountantMixin, self).dispatch(
                request, *args, **kwargs)


def get_attr_121(obj, qry):
    attributes = qry.split('__')
    value = obj
    if value:
        for attr in attributes:
            if attr:
                value = getattr(value, attr)
    else:
        value = 0
    return value


def get_attr_12m(obj, filter_qry):
    filter_qry_list = filter_qry.split('=')
    filter_dict = {}
    filter_dict[filter_qry_list[0]] = filter_qry_list[1]

    value = obj.filter(**filter_dict)
    return value[0] if value else None


def getattr_custom(obj, attr_query, **kwargs):
    # query_example 'tax_details___tax__id=1;__attr___fattr__id=2;__attr2'
    attr_query = attr_query.split(';')
    value = obj
    for query in attr_query:
        queries = query.split('___')
        queries_length = len(queries)
        if queries_length > 1:
            for i, qry in enumerate(queries):
                if i != queries_length - 1:
                    value = get_attr_121(value, qry)
                else:
                    value = get_attr_12m(value, qry)
        else:
            value = get_attr_121(value, query)
    return value


def json_file_to_dict(json_path):
    import json
    data_file = open(json_path)
    return json.load(data_file)


# Report Selector
def get_property_methods(cls):
    property_fields = []
    for field in cls.__dict__.keys():
        if isinstance(cls.__dict__.get(field), property):
            property_fields.append(field)
    return tuple(property_fields)


# Returns base options of model class fields
def get_all_field_options(cls):
    options = []
    for field in cls._meta.get_fields():

        if field.one_to_many or field.many_to_many:
            options.append(
                ('%s___' % (field.name), field.name)
            )
        elif field.many_to_one or field.one_to_one:
            options.append(
                ('%s__' % (field.name), field.name)
            )
        else:
            options.append(
                ('%s' % (field.name), field.name)
            )
    for field in get_property_methods(cls):
        options.append(
            ('%s' % (field), field)
        )
    return tuple(options)

def get_m2m_filter_options(cls):
    options = []
    for field in cls._meta.get_fields():
        if field.many_to_one:
            # TODO ignore main related model
            # TODO (example here is ignore PaymentRecord related  field in case DeductionDetails)
            for obj in field.related_model.objects.all():
                options.append((('%s__id=%s;__') % (field.name, obj.id), (str(obj))))
    return options
