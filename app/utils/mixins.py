import os

from django.contrib import messages
from django.views.generic.edit import UpdateView as BaseUpdateView, CreateView as BaseCreateView, \
    DeleteView as BaseDeleteView
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.template.loader import get_template
from django.template import RequestContext
from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView
from rest_framework.decorators import list_route
from weasyprint import HTML, CSS


def json_from_object(obj):
    data = {
        'id': obj.id
    }

    if hasattr(obj, 'name'):
        data['name'] = obj.name
    elif hasattr(obj, 'title'):
        data['name'] = obj.title
    else:
        data['name'] = str(obj)

    if hasattr(obj, 'percent'):
        data['percent'] = obj.percent  # Percent attr for tax scheme
    return JsonResponse(data)


class AjaxableResponseMixin(object):
    def form_invalid(self, form):
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        response = super(AjaxableResponseMixin, self).form_valid(form)
        if self.request.is_ajax():
            if 'ret' in self.request.GET:
                obj = getattr(self.object, self.request.GET['ret'])
            else:
                obj = self.object
            return json_from_object(obj)
        else:
            return response


def find_static(path):
    from django.contrib.staticfiles import finders
    from django.utils.encoding import smart_unicode

    result = finders.find(path, all=True)
    path = smart_unicode(path)
    if result:
        if not isinstance(result, (list, tuple)):
            result = [result]
        output = u'\n  '.join(
            (smart_unicode(os.path.realpath(path)) for path in result))
        return output


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **kwargs):
        view = super(LoginRequiredMixin, cls).as_view(**kwargs)
        return login_required(view)


class PDFView(TemplateView):
    def get_file_name(self):
        filename = 'download'
        if hasattr(self, 'file_name') and self.file_name:
            filename = self.file_name
        if hasattr(self, 'template_name') and self.template_name:
            from os.path import basename, splitext

            filename = splitext(basename(self.template_name))[0]
        if not filename.endswith('.pdf'):
            filename += '.pdf'
        return filename

    def get_stylesheets(self):
        return [CSS(find_static('css/normalize.css')), CSS(find_static('css/bootstrap/bootstrap.min.css')),
                CSS(find_static('css/base.css')), CSS(find_static('css/pdf.css'))]

    def render_to_response(self, *args, **kwargs):
        html_template = get_template(self.template_name)
        context = {'you': self.request.user, 'pagesize': 'A4'}
        context.update(self.get_context_data())
        rendered_html = html_template.render(RequestContext(self.request, context)).encode(encoding="UTF-8")
        pdf_file = HTML(string=rendered_html).write_pdf(stylesheets=self.get_stylesheets())
        http_response = HttpResponse(pdf_file, content_type='application/pdf')
        http_response['Content-Disposition'] = 'filename="' + self.get_file_name()
        return http_response


class UpdateView(BaseUpdateView):
    def get_context_data(self, **kwargs):
        context = super(UpdateView, self).get_context_data(**kwargs)
        context['scenario'] = _('Update')
        context['base_template'] = 'base.html'
        super(UpdateView, self).get_context_data()
        return context


class CreateView(BaseCreateView):
    def get_context_data(self, **kwargs):
        context = super(CreateView, self).get_context_data(**kwargs)
        context['scenario'] = _('Add')
        if self.request.is_ajax():
            base_template = 'modal.html'
        else:
            base_template = 'base.html'
        context['base_template'] = base_template
        return context


class DeleteView(BaseDeleteView):
    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        response = super(DeleteView, self).post(request, *args, **kwargs)
        messages.success(request,
                         ('%s %s' % (self.object.__class__._meta.verbose_name.title(), _('successfully deleted!'))))
        return response


class TableObjectMixin(TemplateView):
    def get_context_data(self, *args, **kwargs):
        context = super(TableObjectMixin, self).get_context_data(**kwargs)
        if self.kwargs:
            pk = int(self.kwargs.get('pk'))
            obj = get_object_or_404(self.model, pk=pk, company=self.request.company)
            scenario = 'Update'
        else:
            obj = self.model(company=self.request.company)
            # if obj.__class__.__name__ == 'PurchaseVoucher':
            #     tax = self.request.company.settings.purchase_default_tax_application_type
            #     tax_scheme = self.request.company.settings.purchase_default_tax_scheme
            #     if tax:
            #         obj.tax = tax
            #     if tax_scheme:
            #         obj.tax_scheme = tax_scheme
            scenario = 'Create'
        data = self.serializer_class(obj).data
        context['data'] = data
        context['scenario'] = scenario
        context['obj'] = obj
        return context


from functools import reduce
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.db.models import Q
from django.forms import inlineformset_factory
from django.shortcuts import redirect
from django.views.generic import ListView as BaseListView
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.conf import settings


class ListView(BaseListView):
    def __init__(self, *args, **kwargs):
        super(ListView, self).__init__(*args, **kwargs)
        self.redirect_url = None
        self.filter = None

    def get_queryset(self):
        qs = super(ListView, self).get_queryset()
        if self.request.GET.get('q'):
            q = self.request.GET.get('q')
            # Search for exact match
            if self.request.GET.get('q') and hasattr(self, 'search_exact_fields') and self.search_exact_fields:
                search_query = reduce(lambda qr, field: qr | Q(**{field + '__iexact': q}), self.search_fields, Q())
                match_qs = qs.filter(search_query)
                if match_qs.exists():
                    self.redirect_url = match_qs.first().get_absolute_url()
                    return self.model.objects.none()
            # Filter by search query and search fields
            if hasattr(self, 'search_fields') and self.search_fields:
                search_query = reduce(lambda qr, field: qr | Q(**{field + '__icontains': q}), self.search_fields, Q())
                qs = qs.filter(search_query)
        # Use filters to filter the queryset
        if hasattr(self, 'filter_set') and self.filter_set:
            self.filter = self.filter_set(self.request.GET, queryset=qs)
            qs = self.filter.qs
        return qs

    def get_context_data(self, **kwargs):
        context_data = super(ListView, self).get_context_data(**kwargs)
        # Add filter to context data for filter form generation
        if self.filter:
            context_data['filter'] = self.filter
        if (hasattr(self, 'search_fields') and self.search_fields) or (
                    hasattr(self, 'search_exact_fields') and self.search_exact_fields):
            context_data['search'] = True
        return context_data

    def render_to_response(self, context):
        if self.redirect_url:
            return redirect(self.redirect_url)
        return super(ListView, self).render_to_response(context)


# class FormView(SuccessMessageMixin):
#     def get_success_url(self):
#         return self.request.GET.get('next') + '?action=edit' if self.request.GET.get(
#             'next') else super().get_success_url()
#
#     def get_form_class(self):
#         if self.fields and not self.form_class:
#             return modelform_factory(self.get_queryset().model, fields=self.fields)
#         else:
#             return super().get_form_class()
#
#     def get_success_message(self, cleaned_data):
#         klass = self.object.__class__._meta.verbose_name.title().lower()
#         st = str(self.object)
#         if self.scenario == 'Create':
#             return '%s %s "%s" %s.' % (_('New'), klass, st, _('successfully created'))
#         elif self.scenario == 'Edit':
#             return '%s %s "%s" %s.' % (_('Existing'), klass, st, _('successfully updated'))


# class Export(object):
#     def get(self, request, *args, **kwargs):
#         file_name = self.file_name + ' ' + datetime.datetime.today().strftime('%Y-%m-%d') or 'Untitled'
#         export = OpenpyxlExport(file_name)
#         export.generate(self.fields, True)
#         for object in self.queryset:
#             values = [change_format(object, val) for val in self.fields]
#             export.generate(values)
#         export.set_width()
#         return export.response()


# class Import(object):
#     template_name = 'import.html'
#
#     def get_context_data(self, **kwargs):
#         from apps.plant.forms import ImportFile
#
#         context = super(Import, self).get_context_data(**kwargs)
#         context['form'] = ImportFile()
#         return context


class GroupRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super(GroupRequiredMixin, self).dispatch(request, *args, **kwargs)
        if request.user.is_authenticated():
            user_groups = list(self.request.user.groups.values_list('name', flat=True))
            if bool(set(user_groups) & set(self.group_required)):
                return super(GroupRequiredMixin, self).dispatch(request, *args, **kwargs)
        else:
            return redirect(settings.LOGIN_URL)
        raise PermissionDenied()


class FormsetViewMixin(object):
    def get_context_data(self, **kwargs):
        data = super(FormsetViewMixin, self).get_context_data(**kwargs)

        Formset = inlineformset_factory(self.model, self.child_model,
                                        form=self.child_form_class, extra=2)
        instance = self.get_object() if data['scenario'] == "Update" else self.model()

        if self.request.POST:
            data['formset'] = Formset(self.request.POST, self.request.FILES, instance=instance)
        else:
            data['formset'] = Formset(instance=instance)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        with transaction.atomic():
            if form.is_valid() and formset.is_valid():
                self.object = form.save()
                formset.instance = self.object
                formset.save()
            else:
                return super(FormsetViewMixin, self).form_invalid(form)

        return super(FormsetViewMixin, self).form_valid(form)

class InputChoiceMixin(object):
    def get_serializer_class(self):
        if self.action in ('choices',):
            return self.choice_serializer_class
        else:
            return self.serializer_class

    @list_route(methods=['get'])
    def choices(self, request):
        return self.list(request)