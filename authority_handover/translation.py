from modeltranslation.translator import translator, TranslationOptions

from authority_handover.models import AuthorityHandover, BudgetDistribution, Beneficiary, ExpenditureHead


class BeneficiaryTranslationOptions(TranslationOptions):
    fields = ('designation', 'office')



class ExpenditureHeadTranslationOptions(TranslationOptions):
    fields = ('number', 'name',)

translator.register(Beneficiary, BeneficiaryTranslationOptions)
translator.register(BudgetDistribution)
translator.register(ExpenditureHead, ExpenditureHeadTranslationOptions)