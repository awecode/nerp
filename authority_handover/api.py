from rest_framework import viewsets

from app.utils.mixins import InputChoiceMixin
from authority_handover.models import Office, Beneficiary, AuthorityHandover, ExpenditureHead
from authority_handover.serializers import OfficeSerializer, BeneficiarySerializer, AuthorityHandoverSerializer, \
    ExpenditureHeadSerializer, BeneficiaryChoiceSerializer, OfficeChoiceSerializer, AuthorityHandoverChoiceSerializer, \
    ExpenditureHeadChoiceSerializer


class OfficeViewSet(InputChoiceMixin, viewsets.ModelViewSet):
    queryset = Office.objects.all()
    serializer_class = OfficeSerializer
    choice_serializer_class = OfficeChoiceSerializer

    # filter_backends = (filters.DjangoFilterBackend,)
    # filter_fields = ('first_name', 'last_name', 'email', 'username')
    # permission_classes = (UserAccountManagementPerm,)


class BeneficiaryViewSet(InputChoiceMixin, viewsets.ModelViewSet):
    queryset = Beneficiary.objects.all()
    serializer_class = BeneficiarySerializer
    choice_serializer_class = BeneficiaryChoiceSerializer


class AuthorityHandoverViewSet(InputChoiceMixin, viewsets.ModelViewSet):
    queryset = AuthorityHandover.objects.all()
    serializer_class = AuthorityHandoverSerializer
    choice_serializer_class = AuthorityHandoverChoiceSerializer


class ExpenditureHeadViewSet(InputChoiceMixin, viewsets.ModelViewSet):
    queryset = ExpenditureHead.objects.all()
    serializer_class = ExpenditureHeadSerializer
    choice_serializer_class = ExpenditureHeadChoiceSerializer
