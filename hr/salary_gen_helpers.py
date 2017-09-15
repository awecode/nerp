from hr.helpers import get_validity_slots, delta_month_date_impure, month_cnt_inrange
from hr.models import DeductionName, DeductionValidity, Deduction, AllowanceValidity, ProTempore


def combine_deduction_details(deduction_details, added_deduction_details):
    for deduction_detail in deduction_details:
        for added_deduction_detail in added_deduction_details:
            if deduction_detail['deduction'] == added_deduction_detail['deduction']:
                deduction_detail['amount_added_before_deduction'] = added_deduction_detail['amount']
    return deduction_details


def get_incentive(employee, **kwargs):
    if kwargs.get('role') == 'tax_incentive':
        i_filter = {'is_tax_free': False}
    else:
        i_filter = {}
    incentive = 0
    row_errors = []
    # for obj in employee.incentives.all():

    # employee_response['incentive_details'] = []
    incentive_details = []

    i_salary = employee.get_date_range_salary(
        kwargs.get('from_date'),
        kwargs.get('to_date'),
        apply_grade_rate=True
    )

    total_month, total_work_day = delta_month_date_impure(
        kwargs.get('from_date'),
        kwargs.get('to_date')
    )

    for _name in employee.incentives.filter(**i_filter):

        try:
            obj = _name.incentives.all().filter(employee=employee)[0]
            cnt = month_cnt_inrange(
                obj.year_payment_cycle_month,
                kwargs.get('from_date'),
                kwargs.get('to_date')
            )
            if obj.payment_cycle == 'Y':
                # check obj.year_payment_cycle_month to add to salary

                if cnt:
                    if obj.sum_type == 'AMOUNT':
                        incentive_details.append({
                            'amount': round(obj.value * cnt, 3)
                        })
                    else:
                        incentive_details.append({
                            'amount': round(obj.value / 100.0 * i_salary, 3)
                        })
                else:
                    incentive_details.append({
                        'amount': round(0, 3)
                    })

            elif obj.payment_cycle == 'M':
                if obj.sum_type == 'AMOUNT':
                    incentive_details.append({
                        'amount': round(obj.value * total_month, 3)
                    })
                else:
                    incentive_details.append({
                        'amount': round(obj.value / 100.0 * i_salary, 3)
                    })
            elif obj.payment_cycle == 'D':
                if obj.sum_type == 'AMOUNT':
                    incentive_details.append({
                        'amount': round(obj.value * total_work_day, 3)
                    })
                else:
                    # Does this mean percentage in daily wages
                    incentive_details.append({
                        'amount': round(obj.value / 100.0 * i_salary, 3)
                    })
            else:
                # This is hourly case(Dont think we have it)
                incentive_details.append({
                    'amount': round(0, 3)
                })
                # else:
                #     employee_response['incentive_%d' % (_name.id)] = 0
            # Here we should check for scale and calculate from scale
            if _name.with_scale:
                # Get scale here for this employee of this incentive and get value that is
                # scale = none
                # employee_response['incentive_%d' % (_name.id)] = scale / 100 * employee_response['incentive_%d' % (_name.id)]
                pass
        except IndexError:
            row_errors.append('%s not defined for employee %s' % (_name.name, employee.name))
        incentive_details[-1]['incentive'] = _name.id
        incentive_details[-1]['name'] = _name.name
        incentive_details[-1]['editable'] = True if _name.amount_editable else False
        incentive += incentive_details[-1]['amount']
    if kwargs.get('role') == 'tax_incentive' or kwargs.get('request_from_tax_unit'):
        return incentive, row_errors
    return incentive, incentive_details, row_errors


def get_allowance(employee, **kwargs):
    if kwargs.get('role') == 'tax_allowance':
        a_filter = {'is_tax_free': False}
    else:
        a_filter = {}
    allowance_validity_slots = get_validity_slots(AllowanceValidity, kwargs.get('from_date'), kwargs.get('to_date'))

    allowance = 0
    row_errors = []
    # employee_response['allowance_details'] = []
    allowance_details = []
    for _name in employee.allowances.filter(**a_filter):

        allowance_details.append({
            'amount': round(0, 3)
        })

        for slot in allowance_validity_slots:
            try:
                obj = _name.allowances.all().filter(
                    employee_grade=employee.designation.grade,
                    validity_id=slot.validity_id
                )[0]
                total_month, total_work_day = delta_month_date_impure(
                    slot.from_date,
                    slot.to_date
                )
                a_salary = employee.get_date_range_salary(
                    slot.from_date,
                    slot.to_date,
                    apply_grade_rate=True
                )

                if obj.payment_cycle == 'Y':
                    # check obj.year_payment_cycle_month to add to salary
                    cnt = month_cnt_inrange(
                        obj.year_payment_cycle_month,
                        slot.from_date,
                        slot.to_date
                    )
                    if cnt:
                        if obj.sum_type == 'AMOUNT':
                            allowance_details[-1]['amount'] += round(obj.value * cnt, 3)
                        else:
                            allowance_details[-1]['amount'] += round(obj.value / 100.0 * a_salary, 3)
                    else:
                        allowance_details[-1]['amount'] += round(0, 3)

                elif obj.payment_cycle == 'M':
                    if obj.sum_type == 'AMOUNT':
                        allowance_details[-1]['amount'] += round(obj.value * total_month, 3)
                    else:
                        allowance_details[-1]['amount'] += round(obj.value / 100.0 * a_salary, 3)

                elif obj.payment_cycle == 'D':
                    if obj.sum_type == 'AMOUNT':
                        allowance_details[-1]['amount'] += round(obj.value * total_work_day, 3)

                    else:
                        allowance_details[-1]['amount'] += round(obj.value / 100.0 * a_salary, 3)

                allowance += allowance_details[-1]['amount']
            except IndexError:
                validity = AllowanceValidity.objects.get(id=slot.validity_id)
                row_errors.append(
                    '%s data of %s for this employee grade is not available.(%s)[%s]' % (
                        _name, slot, validity, employee.designation.grade)
                )

        allowance_details[-1]['allowance'] = _name.id
        allowance_details[-1]['name'] = _name.name

    if kwargs.get('role') == 'tax_allowance' or kwargs.get('request_from_tax_unit'):
        return allowance, row_errors
    return allowance, allowance_details, row_errors


# Role is either 'addition' or 'deduction'
def get_deduction(employee, **kwargs):
    if kwargs.get('role') == 'deduction' and kwargs.get('request_from_tax_unit') == True:
        d_filter = {'is_tax_free': True}
    else:
        d_filter = {}
    salary_addition_amount = 0
    row_errors = []
    deductions = DeductionName.objects.filter(**d_filter)
    deduction_validity_slots = get_validity_slots(DeductionValidity, kwargs.get('paid_from_date'),
                                                  kwargs.get('paid_to_date'))

    deduction = 0
    # employee_response['deduction_details'] = []
    deduction_details = []
    addition_from_deduction_details = []
    for obj in list(deductions.filter(is_optional=False)) + list(employee.optional_deductions.filter(**d_filter)):

        if kwargs.get('role') == 'deduction':
            deduction_details.append({
                'amount': 0
            })
            for slot in deduction_validity_slots:
                total_month, total_work_day = delta_month_date_impure(
                    slot.from_date,
                    slot.to_date
                )
                slot_salary = employee.get_date_range_salary(
                    slot.from_date,
                    slot.to_date,
                    apply_grade_rate=True
                )
                slot_incentive = get_incentive(employee, from_date=slot.from_date, to_date=slot.to_date)[0]
                slot_allowance = get_allowance(employee, from_date=slot.from_date, to_date=slot.to_date)[0]
                # FIXME may nedd to remove this
                # slot_addition_from_deduction = get_deduction(
                #     employee,
                #     role='addition',
                #     paid_from_date=slot.from_date,
                #     paid_to_date=slot.to_date
                # )[0]
                d_salary = slot_salary + slot_incentive + slot_allowance

                try:
                    deduct_obj = Deduction.objects.filter(validity_id=slot.validity_id, name=obj)[0]

                    if deduct_obj.deduct_type == 'AMOUNT':
                        deduction_details[-1]['amount'] += round(deduct_obj.value * total_month, 3)
                    else:
                        deduction_details[-1]['amount'] += round(deduct_obj.value / 100.0 * d_salary, 3)

                    if employee.type == 'PERMANENT' and obj.first_add_to_salary:
                        deduction_details[-1]['amount'] += deduction_details[-1]['amount']

                    deduction += deduction_details[-1]['amount']
                except IndexError:
                    validity = DeductionValidity.objects.get(id=slot.validity_id)
                    row_errors.append(
                        '%s of %s is not available. (%s)[%s]' % (obj, slot, validity, employee.designation.grade)
                    )
            deduction_details[-1]['deduction'] = obj.id
            deduction_details[-1]['name'] = obj.name
            deduction_details[-1]['editable'] = True if obj.amount_editable else False
        else:
            addition_from_deduction_details.append({
                'amount': 0
            })
            for slot in deduction_validity_slots:
                total_month, total_work_day = delta_month_date_impure(
                    slot.from_date,
                    slot.to_date
                )
                slot_salary = employee.get_date_range_salary(
                    slot.from_date,
                    slot.to_date,
                    apply_grade_rate=True
                )
                slot_incentive = get_incentive(employee, from_date=slot.from_date, to_date=slot.to_date)[0]
                slot_allowance = get_allowance(employee, from_date=slot.from_date, to_date=slot.to_date)[0]
                d_salary = slot_salary + slot_allowance + slot_incentive
                try:
                    deduct_obj = Deduction.objects.filter(validity_id=slot.validity_id, name=obj)[0]

                    if employee.type == 'PERMANENT' and obj.first_add_to_salary:
                        if deduct_obj.deduct_type == 'AMOUNT':
                            salary_addition_amount += deduct_obj.value * total_month
                            addition_from_deduction_details[-1]['amount'] += round(deduct_obj.value * total_month, 3)
                        else:
                            salary_addition_amount += round(deduct_obj.value / 100.0 * d_salary, 3)
                            addition_from_deduction_details[-1]['amount'] += round(deduct_obj.value / 100.0 * d_salary, 3)
                except IndexError:
                    pass
            addition_from_deduction_details[-1]['deduction'] = obj.id
            addition_from_deduction_details[-1]['name'] = obj.name

    if kwargs.get('role') == 'addition':
        if kwargs.get('request_from_tax_unit') == True:
            return salary_addition_amount
        else:
            return salary_addition_amount, addition_from_deduction_details
    else:
        if kwargs.get('request_from_tax_unit') == True:
            return deduction, row_errors
        else:
            return deduction, deduction_details, row_errors


def get_pro_tempore_data(employee):
    # TODO change status when this protempore are transacted
    pro_tempores = ProTempore.objects.filter(pro_tempore_employee=employee, status='READY_FOR_PAYMENT')
    pro_tempore_details = []
    for p_t in pro_tempores:
        pro_tempore_details.append({
            'amount': 0
        })

        pte_salary = p_t.pro_tempore_employee.get_date_range_salary(
            p_t.appoint_date,
            p_t.dismiss_date,
            apply_grade_rate=True
        )
        pte_allowance = get_allowance(p_t.pro_tempore_employee, from_date=p_t.appoint_date, to_date=p_t.dismiss_date)[0]
        pte_total = pte_salary + pte_allowance

        e_salary = p_t.employee.get_date_range_salary(
            p_t.appoint_date,
            p_t.dismiss_date,
            apply_grade_rate=True
        )
        e_allowance = get_allowance(p_t.employee, from_date=p_t.appoint_date,
                                    to_date=p_t.dismiss_date)[0]
        e_total = e_salary + e_allowance

        diff_total = e_total - pte_total
        if diff_total < 0:
            diff_total = 0
        pro_tempore_details[-1]['amount'] = round(diff_total, 3)
        pro_tempore_details[-1]['p_t_id'] = p_t.id
        pro_tempore_details[-1]['appoint_date'] = str(p_t.appoint_date)
        pro_tempore_details[-1]['dismiss_date'] = str(p_t.dismiss_date)
        pro_tempore_details[-1]['employee_name'] = p_t.employee.name
        pro_tempore_details[-1]['employee_designation'] = p_t.employee.designation.designation_name

    return pro_tempore_details
