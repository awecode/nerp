from rest_framework import serializers

from authority_handover.models import Office, Beneficiary, AuthorityHandover, ExpenditureHead, BudgetDistribution, \
    ForeignFund


class OfficeChoiceSerializer(serializers.ModelSerializer):
    label = serializers.ReadOnlyField(source='__str__')
    value = serializers.ReadOnlyField(source='id')

    class Meta:
        model = Office
        fields = ('label', 'value')


class OfficeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Office
        fields = '__all__'


class BeneficiaryChoiceSerializer(serializers.ModelSerializer):
    label = serializers.ReadOnlyField(source='__str__')
    value = serializers.ReadOnlyField(source='id')

    class Meta:
        model = Beneficiary
        fields = ('label', 'value')


class BeneficiarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Beneficiary
        fields = '__all__'


class ExpenditureHeadChoiceSerializer(serializers.ModelSerializer):
    label = serializers.ReadOnlyField(source='__str__')
    value = serializers.ReadOnlyField(source='id')

    class Meta:
        model = ExpenditureHead
        fields = ('label', 'value')


class ExpenditureHeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenditureHead
        fields = '__all__'


class ForeignFundChoiceSerializer(serializers.ModelSerializer):
    label = serializers.ReadOnlyField(source='__str__')
    value = serializers.ReadOnlyField(source='id')

    class Meta:
        model = ForeignFund
        fields = ('label', 'value')


class ForeignFundSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForeignFund
        fields = '__all__'


class BudgetDistributionChoiceSerializer(serializers.ModelSerializer):
    label = serializers.ReadOnlyField(source='__str__')
    value = serializers.ReadOnlyField(source='id')

    class Meta:
        model = BudgetDistribution
        fields = ('label', 'value')


class BudgetDistributionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BudgetDistribution
        fields = '__all__'


class AuthorityHandoverChoiceSerializer(serializers.ModelSerializer):
    label = serializers.ReadOnlyField(source='__str__')
    value = serializers.ReadOnlyField(source='id')

    class Meta:
        model = AuthorityHandover
        fields = ('label', 'value')


class AuthorityHandoverSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthorityHandover
        fields = '__all__'
