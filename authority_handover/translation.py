from modeltranslation.translator import translator, TranslationOptions

from authority_handover.models import AuthorityHandover, BudgetDistribution, Beneficiary


class BeneficiaryTranslationOptions(TranslationOptions):
    fields = ('designation', 'office')

translator.register(Beneficiary, BeneficiaryTranslationOptions)


class BudgetDistributionTranslationOptions(TranslationOptions):
    fields = ('expenditure_head_number', 'expenditure_head_name',)

translator.register(BudgetDistribution, BudgetDistributionTranslationOptions)