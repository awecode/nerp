from rest_framework import viewsets

from authority_handover.models import Office, Beneficiary, AuthorityHandover, ExpenditureHead
from authority_handover.serializers import OfficeSerializer, BeneficiarySerializer, AuthorityHandoverSerializer, \
    ExpenditureHeadSerializer


class OfficeViewSet(viewsets.ModelViewSet):
    queryset = Office.objects.all()
    serializer_class = OfficeSerializer

    # filter_backends = (filters.DjangoFilterBackend,)
    # filter_fields = ('first_name', 'last_name', 'email', 'username')
    # permission_classes = (UserAccountManagementPerm,)


class BeneficiaryViewSet(viewsets.ModelViewSet):
    queryset = Beneficiary.objects.all()
    serializer_class = BeneficiarySerializer


class AuthorityHandoverViewSet(viewsets.ModelViewSet):
    queryset = AuthorityHandover.objects.all()
    serializer_class = AuthorityHandoverSerializer


class ExpenditureHeadViewSet(viewsets.ModelViewSet):
    queryset = ExpenditureHead.objects.all()
    serializer_class = ExpenditureHeadSerializer
