import json
from datetime import date

from django.utils.translation import ugettext as _
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from livesettings import config_value

from inventory.forms import ItemForm, CategoryForm, DemandForm, PartyForm, PurchaseOrderForm, HandoverForm, EntryReportForm
from inventory.filters import InventoryItemFilter
from inventory.models import Demand, DemandRow, delete_rows, Item, Category, Party, PurchaseOrder, PurchaseOrderRow, InventoryAccount, Handover, HandoverRow, EntryReport, EntryReportRow, set_transactions, JournalEntry, InventoryAccountRow
from app.libr import invalid, save_model
from inventory.serializers import DemandSerializer, ItemSerializer, PartySerializer, PurchaseOrderSerializer, HandoverSerializer, EntryReportSerializer, EntryReportRowSerializer, InventoryAccountRowSerializer
from app.nepdate import BSUtil
from users.models import group_required


@login_required
def item_form(request, id=None):
    if id:
        item = get_object_or_404(Item, id=id)
        scenario = 'Update'
    else:
        item = Item()
        scenario = 'Create'
    if request.POST:
        form = ItemForm(data=request.POST, instance=item, user=request.user)
        if form.is_valid():
            item = form.save(commit=False)
            item.save(account_no=form.cleaned_data['account_no'], opening_balance=form.cleaned_data['opening_balance'])
            if request.is_ajax():
                return render(request, 'callback.html', {'obj': ItemSerializer(item).data})
            return redirect('/inventory/items/')
    else:
        form = ItemForm(instance=item, user=request.user)
    if request.is_ajax():
        base_template = 'modal.html'
    else:
        base_template = 'base.html'
    return render(request, 'item_form.html', {
        'scenario': scenario,
        'form': form,
        'base_template': base_template,
    })


@group_required('Store Keeper', 'Chief')
def delete_inventory_item(request, id):
    obj = get_object_or_404(Item, id=id)
    obj.delete()
    return redirect('/inventory/items/')


@group_required('Store Keeper', 'Chief')
def list_inventory_items(request):
    objects = Item.objects.all()
    filtered_items = InventoryItemFilter(request.GET, queryset=objects)
    return render(request, 'list_inventory_items.html', {'objects': filtered_items})


@login_required
def list_demand_forms(request):
    if request.user.in_group('Store Keeper') or request.user.in_group('Chief'):
        objects = Demand.objects.all()
    else:
        objects = Demand.objects.filter(demandee=request.user)
    return render(request, 'list_demand_forms.html', {'objects': objects})


@login_required
def delete_demand(request, id):
    if request.user.in_group('Store Keeper') or request.user.in_group('Chief'):
        obj = get_object_or_404(Demand, id=id)
    else:
        obj = get_object_or_404(Demand, id=id, demandee=request.user)
    obj.delete()
    return redirect(reverse('list_demand_forms'))


@login_required
def items_as_json(request):
    items = Item.objects.all()
    items_data = ItemSerializer(items).data
    return HttpResponse(json.dumps(items_data), mimetype="application/json")


@group_required('Store Keeper', 'Chief')
def list_categories(request):
    categories = Category.objects.filter()
    return render(request, 'list_inventory_categories.html', {'categories': categories})


@group_required('Store Keeper', 'Chief')
def create_category(request):
    category = Category()
    if request.POST:
        form = CategoryForm(data=request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.save()
            return redirect('/inventory/categories/')
    else:
        form = CategoryForm(instance=category)
    if request.is_ajax():
        base_template = 'modal.html'
    else:
        base_template = 'base.html'
    return render(request, 'inventory_category_create_form.html', {
        'form': form,
        'base_template': base_template,
    })


@group_required('Store Keeper', 'Chief')
def update_category(request, id):
    category = get_object_or_404(Category, id=id)
    if request.POST:
        form = CategoryForm(data=request.POST, instance=category)
        if form.is_valid():
            category = form.save(commit=False)
            category.save()
            return redirect('/inventory/categories/')
    else:
        form = CategoryForm(instance=category)
    if request.is_ajax():
        base_template = 'modal.html'
    else:
        base_template = 'base.html'
    return render(request, 'inventory_category_update_form.html', {
        'form': form,
        'base_template': base_template
    })


@group_required('Store Keeper', 'Chief')
def delete_category(request, id):
    category = get_object_or_404(Category, id=id)
    category.delete()
    return redirect('/inventory/categories/')


@login_required
def demand_form(request, id=None):
    if id:
        obj = get_object_or_404(Demand, id=id)
        scenario = 'Update'
    else:
        obj = Demand(date=BSUtil().today(), demandee=request.user)
        scenario = 'Create'
    form = DemandForm(instance=obj)
    object_data = DemandSerializer(obj).data
    return render(request, 'demand_form.html',
                  {'form': form, 'data': object_data, 'scenario': scenario})


@login_required
def save_demand(request):
    params = json.loads(request.body)
    dct = {'rows': {}}
    if params.get('release_no') == '':
        params['release_no'] = None
    object_values = {'release_no': params.get('release_no'), 'fiscal_year': config_value('app', 'fiscal_year'),
                     'date': params.get('date'), 'purpose': params.get('purpose'), 'status': 'Requested'}
    if params.get('id'):
        obj = Demand.objects.get(id=params.get('id'))
    else:
        obj = Demand()
        object_values['demandee_id'] = params.get('demandee')
    try:
        obj = save_model(obj, object_values)
    except Exception as e:
        if hasattr(e, 'messages'):
            dct['error_message'] = '; '.join(e.messages)
        elif str(e) != '':
            dct['error_message'] = str(e)
        else:
            dct['error_message'] = 'Error in form data!'
    dct['id'] = obj.id
    model = DemandRow
    for index, row in enumerate(params.get('table_view').get('rows')):
        if invalid(row, ['item_id', 'quantity', 'unit']):
            continue
        # print row
        # if row.get('release_quantity') == '':
        #     row['release_quantity'] = 1

        values = {'sn': index + 1, 'item_id': row.get('item_id'),
                  'specification': row.get('specification'),
                  'quantity': row.get('quantity'), 'unit': row.get('unit'),
                  'release_quantity': row.get('release_quantity'), 'remarks': row.get('remarks'),
                  'demand': obj}
        submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
        # set_transactions(submodel, request.POST.get('date'),
        #                  ['dr', bank_account, row.get('amount')],
        #                  ['cr', benefactor, row.get('amount')],
        # )
        if not created:
            submodel = save_model(submodel, values)
        dct['rows'][index] = submodel.id
    delete_rows(params.get('table_view').get('deleted_rows'), model)
    return HttpResponse(json.dumps(dct), mimetype="application/json")


@group_required('Store Keeper', 'Chief')
def list_parties(request):
    objects = Party.objects.all()
    return render(request, 'list_parties.html', {'objects': objects})


@group_required('Store Keeper', 'Chief')
def party_form(request, id=None):
    if id:
        obj = get_object_or_404(Party, id=id)
        scenario = 'Update'
    else:
        obj = Party()
        scenario = 'Create'
    if request.POST:
        form = PartyForm(data=request.POST, instance=obj)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            if request.is_ajax():
                return render(request, 'callback.html', {'obj': PartySerializer(obj).data})
            return redirect(reverse('list_parties'))
    else:
        form = PartyForm(instance=obj)
    if request.is_ajax():
        base_template = 'modal.html'
    else:
        base_template = 'base.html'
    return render(request, 'party_form.html', {
        'scenario': scenario,
        'form': form,
        'base_template': base_template,
    })


@group_required('Store Keeper', 'Chief')
def delete_party(request, id):
    obj = get_object_or_404(Party, id=id)
    obj.delete()
    return redirect(reverse('list_parties'))


@group_required('Store Keeper', 'Chief')
def parties_as_json(request):
    objects = Party.objects.all()
    objects_data = PartySerializer(objects).data
    return HttpResponse(json.dumps(objects_data), mimetype="application/json")


@group_required('Store Keeper', 'Chief')
def purchase_order(request, id=None):
    if id:
        obj = get_object_or_404(PurchaseOrder, id=id)
        scenario = 'Update'
    else:
        obj = PurchaseOrder(date=BSUtil().today())
        scenario = 'Create'
    form = PurchaseOrderForm(instance=obj)
    object_data = PurchaseOrderSerializer(obj).data
    return render(request, 'purchase_order.html',
                  {'form': form, 'data': object_data, 'scenario': scenario})


@group_required('Store Keeper', 'Chief')
def save_purchase_order(request):
    params = json.loads(request.body)
    dct = {'rows': {}}
    object_values = {'order_no': params.get('order_no'), 'fiscal_year': config_value('app', 'fiscal_year'),
                     'date': params.get('date'), 'party_id': params.get('party'),
                     'due_days': params.get('due_days')}
    if params.get('id'):
        obj = PurchaseOrder.objects.get(id=params.get('id'))
    else:
        obj = PurchaseOrder()
    try:
        obj = save_model(obj, object_values)
    except Exception as e:
        if hasattr(e, 'messages'):
            dct['error_message'] = '; '.join(e.messages)
        elif str(e) != '':
            dct['error_message'] = str(e)
        else:
            dct['error_message'] = 'Error in form data!'
    dct['id'] = obj.id
    model = PurchaseOrderRow
    for index, row in enumerate(params.get('table_view').get('rows')):
        if invalid(row, ['quantity', 'unit', 'rate', 'item_id']):
            continue
        if row.get('budget_title_no') == '':
            row['budget_title_no'] = None
        values = {'sn': index + 1, 'item_id': row.get('item_id'),
                  'specification': row.get('specification'), 'rate': row.get('rate'),
                  'quantity': row.get('quantity'), 'unit': row.get('unit'),
                  'budget_title_no': row.get('budget_title_no'), 'remarks': row.get('remarks'),
                  'purchase_order': obj}
        submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
        # set_transactions(submodel, request.POST.get('date'),
        #                  ['dr', bank_account, row.get('amount')],
        #                  ['cr', benefactor, row.get('amount')],
        # )
        if not created:
            submodel = save_model(submodel, values)
        dct['rows'][index] = submodel.id
    delete_rows(params.get('table_view').get('deleted_rows'), model)
    return HttpResponse(json.dumps(dct), mimetype="application/json")


@group_required('Store Keeper', 'Chief')
def list_purchase_orders(request):
    objects = PurchaseOrder.objects.all()
    return render(request, 'list_purchase_orders.html', {'objects': objects})


@group_required('Store Keeper', 'Chief')
def delete_purchase_order(request, id):
    obj = get_object_or_404(PurchaseOrder, id=id)
    obj.delete()
    return redirect(reverse('list_purchase_orders'))


@group_required('Store Keeper', 'Chief')
def list_inventory_accounts(request):
    objects = InventoryAccount.objects.all()
    return render(request, 'list_inventory_accounts.html', {'objects': objects})


@group_required('Store Keeper', 'Chief')
def list_consumable_accounts(request):
    objects = InventoryAccount.objects.filter(item__type='consumable')
    return render(request, 'list_consumable_inventory_accounts.html', {'objects': objects})


@group_required('Store Keeper', 'Chief')
def list_non_consumable_accounts(request):
    objects = InventoryAccount.objects.filter(item__type='non-consumable')
    return render(request, 'list_non_consumable_inventory_accounts.html', {'objects': objects})


@group_required('Store Keeper', 'Chief')
def view_inventory_account(request, id):
    obj = get_object_or_404(InventoryAccount, id=id)
    journal_entries = JournalEntry.objects.filter(transactions__account_id=obj.id).order_by('id', 'date') \
        .prefetch_related('transactions', 'content_type', 'transactions__account').select_related()
    data = InventoryAccountRowSerializer(journal_entries).data
    return render(request, 'view_inventory_account.html', {'obj': obj, 'entries': journal_entries, 'data': data})


@group_required('Store Keeper', 'Chief')
def handover_incoming(request, id=None):
    if id:
        obj = get_object_or_404(Handover, id=id)
        scenario = 'Update'
    else:
        obj = Handover(date=BSUtil().today(), type='Incoming')
        scenario = 'Create'
    form = HandoverForm(instance=obj)
    object_data = HandoverSerializer(obj).data
    return render(request, 'handover.html',
                  {'form': form, 'data': object_data, 'scenario': scenario})


@group_required('Store Keeper', 'Chief')
def handover_outgoing(request, id=None):
    if id:
        obj = get_object_or_404(Handover, id=id)
        scenario = 'Update'
    else:
        obj = Handover(date=BSUtil().today(), type='Outgoing')
        scenario = 'Create'
    form = HandoverForm(instance=obj)
    object_data = HandoverSerializer(obj).data
    return render(request, 'handover.html',
                  {'form': form, 'data': object_data, 'scenario': scenario})


@group_required('Store Keeper', 'Chief')
def save_handover(request):
    params = json.loads(request.body)
    dct = {'rows': {}}
    object_values = {'addressee': params.get('addressee'), 'fiscal_year': config_value('app', 'fiscal_year'),
                     'date': params.get('date'), 'office': params.get('office'), 'type': params.get('type'),
                     'designation': params.get('designation'), 'voucher_no': params.get('voucher_no'),
                     'due_days': params.get('due_days'), 'handed_to': params.get('handed_to')}
    if params.get('id'):
        obj = Handover.objects.get(id=params.get('id'))
    else:
        obj = Handover()
    try:
        obj = save_model(obj, object_values)
    except Exception as e:
        if hasattr(e, 'messages'):
            dct['error_message'] = '; '.join(e.messages)
        elif str(e) != '':
            dct['error_message'] = str(e)
        else:
            dct['error_message'] = 'Error in form data!'
    dct['id'] = obj.id
    model = HandoverRow
    for index, row in enumerate(params.get('table_view').get('rows')):
        if invalid(row, ['quantity', 'unit', 'item_id', 'total_amount']):
            continue
        values = {'sn': index + 1, 'item_id': row.get('item_id'),
                  'specification': row.get('specification'),
                  'quantity': row.get('quantity'), 'unit': row.get('unit'), 'received_date': row.get('received_date'),
                  'total_amount': row.get('total_amount'), 'condition': row.get('condition'),
                  'handover': obj}
        submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
        if not created:
            submodel = save_model(submodel, values)
        dct['rows'][index] = submodel.id
    delete_rows(params.get('table_view').get('deleted_rows'), model)
    return HttpResponse(json.dumps(dct), mimetype="application/json")


@group_required('Store Keeper', 'Chief')
def list_incoming_handovers(request):
    objects = Handover.objects.filter(type='Incoming')
    return render(request, 'list_incoming_handovers.html', {'objects': objects})


@group_required('Store Keeper', 'Chief')
def list_outgoing_handovers(request):
    objects = Handover.objects.filter(type='Outgoing')
    return render(request, 'list_outgoing_handovers.html', {'objects': objects})


@group_required('Store Keeper', 'Chief')
def handover_entry_report(request, id=None):
    source = get_object_or_404(Handover, id=id, type='Incoming')
    if source.get_entry_report():
        report = source.get_entry_report()
        object_data = EntryReportSerializer(report).data
    else:
        report = EntryReport()
        object_data = EntryReportSerializer(report).data
        report.fiscal_year = source.fiscal_year
        report.source = source
        all_rows = []
        for r in source.rows.all():
            row = EntryReportRow()
            row.sn = r.sn
            row.item = r.item
            row.specification = r.specification
            row.quantity = r.quantity
            row.unit = r.unit
            row.rate = r.total_amount / r.quantity
            row.remarks = r.condition
            row_data = EntryReportRowSerializer(row).data
            all_rows.append(row_data)
        object_data.update({'rows': all_rows})
    form = EntryReportForm(instance=report)
    object_data['type'] = 'handover'
    object_data['source_id'] = source.id
    return render(request, 'entry_report.html',
                  {'form': form, 'data': object_data})


@group_required('Store Keeper', 'Chief')
def purchase_entry_report(request, id=None):
    source = get_object_or_404(PurchaseOrder, id=id)
    if source.get_entry_report():
        report = source.get_entry_report()
        object_data = EntryReportSerializer(report).data
    else:
        report = EntryReport()
        object_data = EntryReportSerializer(report).data
        report.fiscal_year = source.fiscal_year
        report.source = source
        all_rows = []
        for r in source.rows.all():
            row = EntryReportRow()
            row.sn = r.sn
            row.item = r.item
            row.specification = r.specification
            row.quantity = r.quantity
            row.unit = r.unit
            row.rate = r.rate
            row.remarks = r.remarks
            row_data = EntryReportRowSerializer(row).data
            all_rows.append(row_data)
        object_data.update({'rows': all_rows})
    form = EntryReportForm(instance=report)
    object_data['type'] = 'purchase'
    object_data['source_id'] = source.id
    return render(request, 'entry_report.html',
                  {'form': form, 'data': object_data})


@group_required('Store Keeper', 'Chief')
def save_entry_report(request):
    params = json.loads(request.body)
    dct = {'rows': {}}
    if params.get('type') == 'handover':
        source = Handover.objects.get(id=params.get('source_id'))
    else:
        source = PurchaseOrder.objects.get(id=params.get('source_id'))
    object_values = {'entry_report_no': params.get('entry_report_no'),
                     'fiscal_year': config_value('app', 'fiscal_year'),
                     'source': source}
    if params.get('id'):
        obj = EntryReport.objects.get(id=params.get('id'))
    else:
        obj = EntryReport()
    try:
        obj = save_model(obj, object_values)
    except Exception as e:
        if hasattr(e, 'messages'):
            dct['error_message'] = '; '.join(e.messages)
        elif str(e) != '':
            dct['error_message'] = str(e)
        else:
            dct['error_message'] = 'Error in form data!'
    dct['id'] = obj.id
    model = EntryReportRow
    for index, row in enumerate(params.get('table_view').get('rows')):
        if invalid(row, ['quantity', 'unit', 'item_id', 'rate']):
            continue
        if row.get('other_expenses') == '':
            other_expenses = 0
        else:
            other_expenses = row.get('other_expenses')
        values = {'sn': index + 1, 'item_id': row.get('item_id'),
                  'specification': row.get('specification'),
                  'quantity': row.get('quantity'), 'unit': row.get('unit'), 'rate': row.get('rate'),
                  'remarks': row.get('remarks'), 'other_expenses': other_expenses,
                  'entry_report': obj}
        submodel, created = model.objects.get_or_create(id=row.get('id'), defaults=values)
        if not created:
            submodel = save_model(submodel, values)
        dct['rows'][index] = submodel.id
        set_transactions(submodel, obj.source.date,
                         ['dr', submodel.item.account, submodel.quantity],
        )
    delete_rows(params.get('table_view').get('deleted_rows'), model)
    return HttpResponse(json.dumps(dct), mimetype="application/json")


@group_required('Store Keeper', 'Chief')
def list_entry_reports(request):
    objects = EntryReport.objects.all()
    return render(request, 'list_entry_reports.html', {'objects': objects})


@group_required('Store Keeper', 'Chief')
def list_handover_entry_reports(request):
    objects = EntryReport.objects.filter(source_content_type__model='handover')
    return render(request, 'list_entry_reports.html', {'objects': objects})


@group_required('Store Keeper', 'Chief')
def list_purchase_entry_reports(request):
    objects = EntryReport.objects.filter(source_content_type__model='purchaseorder')
    return render(request, 'list_entry_reports.html', {'objects': objects})


@group_required('Store Keeper', 'Chief')
def delete_entry_report(request, id):
    obj = get_object_or_404(EntryReport, id=id)
    obj.delete()
    return redirect(reverse('list_entry_reports'))


@group_required('Store Keeper', 'Chief')
def approve_demand(request):
    params = json.loads(request.body)
    dct = {'rows': {}}
    if params.get('id'):
        row = DemandRow.objects.get(id=params.get('id'))
    else:
        dct['error_message'] = 'Row needs to be saved before being approved!'
        return HttpResponse(json.dumps(dct), mimetype="application/json")
    if not invalid(params, ['item_id', 'quantity', 'unit', 'release_quantity']):
        values = {'item_id': params.get('item_id'),
                  'specification': params.get('specification'),
                  'quantity': params.get('quantity'), 'unit': params.get('unit'),
                  'release_quantity': params.get('release_quantity'), 'remarks': params.get('remarks')}
        row = save_model(row, values)
    row.status = 'Approved'
    row.save()
    return HttpResponse(json.dumps(dct), mimetype="application/json")


@group_required('Store Keeper', 'Chief')
def disapprove_demand(request):
    params = json.loads(request.body)
    dct = {}
    if params.get('id'):
        row = DemandRow.objects.get(id=params.get('id'))
    else:
        dct['error_message'] = 'Voucher needs to be saved before being disapproved!'
        return HttpResponse(json.dumps(dct), mimetype="application/json")
    row.status = 'Requested'
    row.save()
    return HttpResponse(json.dumps(dct), mimetype="application/json")


@group_required('Store Keeper', 'Chief')
def fulfill_demand(request):
    params = json.loads(request.body)
    dct = {}
    if params.get('id'):
        row = DemandRow.objects.get(id=params.get('id'))
    else:
        dct['error_message'] = 'Row needs to be saved before being fulfilled!'
        return HttpResponse(json.dumps(dct), mimetype="application/json")
    if params['status'] == 'Requested':
        dct['error_message'] = 'Row needs to be approved before being fulfilled!'
        return HttpResponse(json.dumps(dct), mimetype="application/json")
    set_transactions(row, row.demand.date,
                     ['cr', row.item.account, row.release_quantity],
    )
    row.status = 'Fulfilled'
    row.save()
    return HttpResponse(json.dumps(dct), mimetype="application/json")


@group_required('Store Keeper', 'Chief')
def unfulfill_demand(request):
    params = json.loads(request.body)
    dct = {}
    if params.get('id'):
        row = DemandRow.objects.get(id=params.get('id'))
    else:
        dct['error_message'] = 'Row needs to be saved before being unfulfilled!'
        return HttpResponse(json.dumps(dct), mimetype="application/json")
    if params['status'] != 'Fulfilled':
        dct['error_message'] = 'Row needs to be fulfilled before being unfulfilled!'
        return HttpResponse(json.dumps(dct), mimetype="application/json")
    journal_entry = JournalEntry.get_for(row)
    journal_entry.delete()
    row.status = 'Approved'
    row.save()
    return HttpResponse(json.dumps(dct), mimetype="application/json")


@group_required('Store Keeper', 'Chief')
def save_account(request):
    params = json.loads(request.body)
    dct = {'rows': {}}
    for index, row in enumerate(params.get('table_vm').get('rows')):
        entry = JournalEntry.objects.get(id=row.get('id'))
        try:
            account_row = entry.account_row
        except:
            account_row = InventoryAccountRow(journal_entry=entry)
        if row.get('expense_total_cost_price') == '':
            row['expense_total_cost_price'] = None
        if row.get('remaining_total_cost_price') == '':
            row['remaining_total_cost_price'] = None
        values = {'country_of_production_or_company_name': row.get('country_or_company'), 'size': row.get('size'),
                  'expected_life': row.get('expected_life'), 'source': row.get('source'), 'remarks': row.get('remarks'),
                  'expense_total_cost_price': row.get('expense_total_cost_price'),
                  'remaining_total_cost_price': row.get('remaining_total_cost_price')}
        account_row = save_model(account_row, values)
    return HttpResponse(json.dumps(dct), mimetype="application/json")