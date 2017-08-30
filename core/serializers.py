# -*- coding: utf-8 -*-
from rest_framework import serializers

from core.models import Employee, Donor, Activity, BudgetHead, TaxScheme, BudgetBalance, Language


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee


class DonorChoiceSerializer(serializers.ModelSerializer):
    label = serializers.ReadOnlyField(source='__unicode__')
    value = serializers.ReadOnlyField(source='id')

    class Meta:
        model = Donor
        fields = ('label', 'value')


class DonorSerializer(serializers.ModelSerializer):
    # name = serializers.Field(source='name')

    class Meta:
        model = Donor


class ActivitySerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='__unicode__')

    class Meta:
        model = Activity


class BudgetBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = BudgetBalance
        exclude = ['id', 'budget_head', 'fiscal_year', 'nepal_government', 'foreign_cash_grant', 'foreign_cash_loan',
                   'foreign_compensating_grant', 'foreign_compensating_loan', 'foreign_substantial_aid']


class BudgetHeadChoiceSerializer(serializers.ModelSerializer):
    label = serializers.ReadOnlyField(source='__unicode__')
    value = serializers.ReadOnlyField(source='id')

    class Meta:
        model = BudgetHead
        fields = ('label', 'value')


class BudgetSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='__unicode__')
    current_balance = BudgetBalanceSerializer()

    class Meta:
        model = BudgetHead


class TaxSchemeSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='__unicode__')

    class Meta:
        model = TaxScheme


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
