from hr.models import PayrollConfig
from django import template

register = template.Library()


@register.assignment_tag
def conf_has_category():
    config = PayrollConfig.get_solo()
    fields = (
        'pay_head_account_category',
        'deduction_account_category',
        'allowance_account_category',
        'incentive_account_category',
        'basic_salary_account_category',
        'tax_account_category',
        'salary_giving_account_category',
        'pro_tempore_account_category'
    )
    for field in fields:
        if getattr(config, field):
            pass
        else:
            return False
    return True
