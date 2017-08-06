from app.utils.forms import HTML5BootstrapModelForm, BootstrapModelForm
from authority_handover.models import AuthorityHandover, BudgetDistribution


class AuthorityHandoverForm(HTML5BootstrapModelForm):
    class Meta:
        model = AuthorityHandover
        fields = (
            'beneficiary_designation',
            'beneficiary_office',
            'fiscal_year',
            'budget_head',
            'priority_code', 'date'
        )


class BudgetDistributionForm(BootstrapModelForm):
    class Meta:
        model = BudgetDistribution
        fields = (
            'expenditure_head_number',
            'expenditure_head_name',
            'permitted_budget',
            'government_fund',
            'foreign_fund_grant_cash',
            'foreign_fund_grant_reimbursable',
            'foreign_fund_grant_direct_payment',
            'foreign_fund_grant_commodity',
            'foreign_fund_loan_cash',
            'foreign_fund_loan_reimbursable',
            'foreign_fund_loan_direct_payment',
            # 'foreign_fund_loan_commodity',
            'donor',
            'remarks'
        )
