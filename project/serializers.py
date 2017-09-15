from rest_framework import serializers

from models import ImprestTransaction, ExpenseRow, ExpenseCategory, Expense, BudgetAllocationItem, Aid, \
    ImprestJournalVoucher, \
    DisbursementDetail, DisbursementParticulars


class ImprestTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImprestTransaction


class ExpenseRowSerializer(serializers.ModelSerializer):
    # category_id = serializers.Field()

    class Meta:
        model = ExpenseRow


class ExpenseCategorySerializer(serializers.ModelSerializer):
    url = serializers.ReadOnlyField(source='get_absolute_url')

    class Meta:
        model = ExpenseCategory


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense


class AidSerializer(serializers.ModelSerializer):
    aid_name = serializers.SerializerMethodField()

    class Meta:
        model = Aid

    def get_aid_name(self, obj):
        return str(obj.id) + '-' + obj.donor.name


class BaseStatementSerializer(serializers.ModelSerializer):
    budget_head_id = serializers.ReadOnlyField(source='budget_head.id')
    aid_name = serializers.SerializerMethodField()
    recurrent = serializers.ReadOnlyField(source='budget_head.recurrent')

    class Meta:
        model = BudgetAllocationItem
        exclude = ('budget_head', 'aid',)

    def get_aid_name(self, obj):
        name = None
        if obj.aid:
            name = str(obj.aid.id) + '-' + obj.aid.donor.name
        return name


class ImprestJVSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImprestJournalVoucher


class DisbursementParticularsSerializer(serializers.ModelSerializer):
    expense_category_id = serializers.ReadOnlyField(source='expense_category.id')

    class Meta:
        model = DisbursementParticulars


class DisbursementDetailSerializer(serializers.ModelSerializer):
    aid_id = serializers.ReadOnlyField()
    rows = DisbursementParticularsSerializer(many=True)
    requested_date = serializers.DateField(format=None)

    class Meta:
        model = DisbursementDetail
        exclude = ('aid',)
