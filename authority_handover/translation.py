from modeltranslation.translator import translator, TranslationOptions

from authority_handover.models import AuthorityHandover, BudgetDistribution


class AuthorityHandoverTranslationOptions(TranslationOptions):
    fields = ('beneficiary_designation', 'beneficiary_office')

translator.register(AuthorityHandover, AuthorityHandoverTranslationOptions)


class BudgetDistributionTranslationOptions(TranslationOptions):
    fields = ('expenditure_head_number', 'expenditure_head_name',)

translator.register(BudgetDistribution, BudgetDistributionTranslationOptions)