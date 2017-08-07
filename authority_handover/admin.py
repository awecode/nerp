from django.contrib import admin

from authority_handover.models import AuthorityHandover, BudgetDistribution, Beneficiary

admin.site.register(AuthorityHandover)

admin.site.register(BudgetDistribution)
admin.site.register(Beneficiary)