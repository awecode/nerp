from rest_framework import serializers
from inventory.models import Demand, DemandRow, Item, Party, PurchaseOrder, PurchaseOrderRow, HandoverRow, Handover, EntryReport, EntryReportRow, JournalEntry


class ItemSerializer(serializers.ModelSerializer):
    account_no = serializers.Field(source='account.account_no')

    class Meta:
        model = Item


class PartySerializer(serializers.ModelSerializer):
    class Meta:
        model = Party


class DemandRowSerializer(serializers.ModelSerializer):
    item_id = serializers.Field(source='item.id')

    class Meta:
        model = DemandRow
        exclude = ['item']


class DemandSerializer(serializers.ModelSerializer):
    rows = DemandRowSerializer()

    class Meta:
        model = Demand


class PurchaseOrderRowSerializer(serializers.ModelSerializer):
    item_id = serializers.Field(source='item.id')

    class Meta:
        model = PurchaseOrderRow


class PurchaseOrderSerializer(serializers.ModelSerializer):
    rows = PurchaseOrderRowSerializer()

    class Meta:
        model = PurchaseOrder


class HandoverRowSerializer(serializers.ModelSerializer):
    item_id = serializers.Field(source='item.id')

    class Meta:
        model = HandoverRow


class HandoverSerializer(serializers.ModelSerializer):
    rows = HandoverRowSerializer()

    class Meta:
        model = Handover


class EntryReportRowSerializer(serializers.ModelSerializer):
    item_id = serializers.Field(source='item.id')

    class Meta:
        model = EntryReportRow
        exclude = ['item']


class EntryReportSerializer(serializers.ModelSerializer):
    rows = EntryReportRowSerializer()

    class Meta:
        model = EntryReport


class InventoryAccountRowSerializer(serializers.ModelSerializer):
    voucher_no = serializers.Field(source='creator.get_voucher_no')
    specification = serializers.Field(source='creator.specification')
    country_or_company = serializers.SerializerMethodField('get_country_or_company')
    size = serializers.SerializerMethodField('get_size')
    expected_life = serializers.SerializerMethodField('get_expected_life')
    source = serializers.SerializerMethodField('get_source')
    income_quantity = serializers.SerializerMethodField('get_income_quantity')
    income_rate = serializers.SerializerMethodField('get_income_rate')
    income_total = serializers.SerializerMethodField('get_income_total')
    expense_quantity = serializers.SerializerMethodField('get_expense_quantity')
    expense_total_cost_price = serializers.SerializerMethodField('get_expense_total_cost_price')
    remaining_total_cost_price = serializers.SerializerMethodField('get_remaining_total_cost_price')
    remarks = serializers.SerializerMethodField('get_remarks')

    class Meta:
        model = JournalEntry

    def get_country_or_company(self, obj):
        try:
            return obj.account_row.country_of_production_or_company_name
        except:
            return None

    def get_size(self, obj):
        try:
            return obj.account_row.size
        except:
            return None

    def get_expected_life(self, obj):
        try:
            return obj.account_row.expected_life
        except:
            return None

    def get_source(self, obj):
        try:
            return obj.account_row.source
        except:
            return None

    def get_income_quantity(self, obj):
        if obj.creator.__class__ == DemandRow:
            return None
        return obj.creator.quantity

    def get_income_rate(self, obj):
        if obj.creator.__class__ == DemandRow:
            return None
        return obj.creator.rate

    def get_income_total(self, obj):
        if obj.creator.__class__ == DemandRow:
            return None
        import math

        return math.ceil(obj.creator.total_entry_cost() * 100) / 100

    def get_expense_quantity(self, obj):
        if obj.creator.__class__ == EntryReportRow:
            return None
        return obj.creator.quantity

    def get_expense_total_cost_price(self, obj):
        try:
            return obj.account_row.expense_total_cost_price
        except:
            return None

    def get_remaining_total_cost_price(self, obj):
        try:
            return obj.account_row.remaining_total_cost_price
        except:
            return None


    def get_remarks(self, obj):
        try:
            return obj.account_row.remarks
        except:
            return None