from app.utils.forms import HTML5BootstrapModelForm, BootstrapModelForm
from authority_handover.models import AuthorityHandover, BudgetDistribution


class AuthorityHandoverForm(HTML5BootstrapModelForm):
    class Meta:
        model = AuthorityHandover
        fields = "__all__"


class BudgetDistributionForm(BootstrapModelForm):
    class Meta:
        model = BudgetDistribution
        fields = "__all__"
