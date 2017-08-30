from django.contrib import admin

from authority_handover.models import AuthorityHandover, BudgetDistribution, Beneficiary, ForeignFund, ExpenditureHead, \
    Office, District

admin.site.register(AuthorityHandover)

admin.site.register(BudgetDistribution)
admin.site.register(ForeignFund)
admin.site.register(Beneficiary)
admin.site.register(ExpenditureHead)
admin.site.register(Office)
admin.site.register(District)