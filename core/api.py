from rest_framework import viewsets

from app.utils.mixins import InputChoiceMixin
from core.models import BudgetHead, Donor
from core.serializers import BudgetSerializer, BudgetHeadChoiceSerializer, DonorSerializer, DonorChoiceSerializer


class BudgetHeadViewSet(InputChoiceMixin, viewsets.ModelViewSet):
    queryset = BudgetHead.objects.all()
    serializer_class = BudgetSerializer
    choice_serializer_class = BudgetHeadChoiceSerializer

    # filter_backends = (filters.DjangoFilterBackend,)
    # filter_fields = ('first_name', 'last_name', 'email', 'username')
    # permission_classes = (UserAccountManagementPerm,)


class DonorViewSet(InputChoiceMixin, viewsets.ModelViewSet):
    queryset = Donor.objects.all()
    serializer_class = DonorSerializer
    choice_serializer_class = DonorChoiceSerializer

    # filter_backends = (filters.DjangoFilterBackend,)
    # filter_fields = ('first_name', 'last_name', 'email', 'username')
    # permission_classes = (UserAccountManagementPerm,)

