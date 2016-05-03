import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import ListView

from app.utils.helpers import save_model
from core.models import FiscalYear
from inventory.models import delete_rows
from models import ImprestTransaction
from serializers import ImprestTransactionSerializer


def imprest_ledger(request):
    context = {
        'fy': FiscalYear.get()
    }
    return render(request, 'imprest_ledger.html', context)


class ImprestLedger(ListView):
    model = ImprestTransaction
    template_name = 'imprest_ledger.html'
    fy = None

    def get_fy(self):
        if not self.fy:
            self.fy = FiscalYear.get()
        return self.fy

    def get_context_data(self, **kwargs):
        context_data = super(ImprestLedger, self).get_context_data(**kwargs)
        context_data['fy'] = self.get_fy()
        context_data['data'] = {
            'fy_id': self.get_fy().id,
            'rows': ImprestTransactionSerializer(context_data['object_list'], many=True).data,
        }
        return context_data

    def get_queryset(self):
        qs = super(ImprestLedger, self).get_queryset()
        qs = qs.filter(fy=self.get_fy())
        return qs


@login_required
def save_imprest_ledger(request):
    params = json.loads(request.body)
    dct = {'rows': {}}
    model = ImprestTransaction
    fy_id = params.get('fy_id')
    try:
        for index, row in enumerate(params.get('table_view').get('rows')):
            values = {'date': row.get('date', ''),
                      'name': row.get('name'),
                      'type': row.get('type'),
                      'date_of_payment': row.get('date_of_payment', ''),
                      'wa_no': row.get('wa_no'),
                      'amount_nrs': row.get('amount_nrs', None),
                      'amount_usd': row.get('amount_usd', None),
                      'exchange_rate': row.get('exchange_rate', None),
                      'fy_id': fy_id
                      }
            submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
            if not created:
                submodel = save_model(submodel, values)
            dct['rows'][index] = submodel.id

            # if submodel.handover.type == 'Outgoing':
            #     set_transactions(submodel, submodel.handover.date,
            #                      ['cr', submodel.item.account, submodel.quantity]
            #                      , )
    except Exception as e:
        if hasattr(e, 'messages'):
            dct['error_message'] = '; '.join(e.messages)
        elif str(e) != '':
            dct['error_message'] = str(e)
        else:
            dct['error_message'] = 'Error in form data!'
    delete_rows(params.get('table_view').get('deleted_rows'), model)
    return JsonResponse(dct)
