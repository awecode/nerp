import django_filters

from app.utils.forms import BootstrapForm
from authority_handover.models import AuthorityHandover


class AuthorityHandoverFilter(django_filters.FilterSet):
    class Meta:
        model = AuthorityHandover
        fields = []
        form = BootstrapForm