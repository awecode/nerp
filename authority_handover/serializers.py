from rest_framework import serializers

from authority_handover.models import Office, Beneficiary, AuthorityHandover, ExpenditureHead, BudgetDistribution


class OfficeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Office
        fields = '__all__'


class BeneficiarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Beneficiary
        fields = '__all__'


class ExpenditureHeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenditureHead
        fields = '__all__'


class ForeignFundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Beneficiary
        fields = '__all__'


class BudgetDistributionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BudgetDistribution
        fields = '__all__'


class AuthorityHandoverSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthorityHandover
        fields = '__all__'
