from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from app.utils.helpers import title_case
from core.models import Language
from ils.forms import RecordForm, BookForm,\
     PublisherForm, OutgoingForm, IncomingForm, PatronForm
from ils.serializers import TransactionSerializer
# from ils.models import library_setting as setting
from ils.models import LibrarySetting

from . import isbn as isbnpy
import urllib2
import urllib
import json
import re
from django.utils import timezone
import datetime
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import Record, Author, Publisher, Book, Subject,\
    Place, BookFile, Transaction

import os
from django.utils.decorators import method_decorator
# from datetime import datetime
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from users.models import User, group_required
# from haystack.query import SearchQuerySet
from ils.forms import LibrarySearchForm


from django.http import HttpResponseRedirect


@group_required('Librarian')
def outgoing(request, pk=None):
    transaction = Transaction.new()
    if pk:
        transaction.record = Record.objects.get(id=pk)
    form = OutgoingForm(instance=transaction)
    return render(request, 'outgoing.html', {'form': form})


@group_required('Librarian')
def save_outgoing(request):
    error = False
    transaction = Transaction.new()
    transaction.user_id = request.POST.get('user')
    transaction.borrow_date = request.POST.get('borrow_date')
    transaction.due_date = request.POST.get('due_date')
    transaction.record_id = request.POST.get('record')
    if request.POST.get('isbn'):
        isbn = request.POST.get('isbn')
        if isbnpy.isValid(isbn):
            if isbnpy.isI10(isbn):
                isbn = isbnpy.convert(isbn)
            try:
                transaction.record = Record.objects.get(isbn13=isbn)
            except Record.DoesNotExist:
                error = 'No books with provided ISBN in library database.'
        else:
            error = 'Invalid ISBN!'
        if error:
            raise Exception(error)
    transaction.save()
    messages.success(request, 'Checked Out!')
    return redirect(
        reverse_lazy(
            'view_record',
            kwargs={
                'pk': transaction.record_id}))


@group_required('Librarian')
def incoming(request, transaction_pk):
    transaction = Transaction.objects.get(id=transaction_pk)
    if request.POST:

        form = IncomingForm(data=request.POST, instance=transaction)
        transaction = form.save()
        if not request.POST.get('return_date'):
            transaction.return_date = datetime.datetime.today()
        transaction.save()
        messages.success(request, 'Book Returned!')
        return redirect(
            reverse_lazy(
                'view_record',
                kwargs={
                    'pk': transaction.record_id}))

    form = IncomingForm(instance=transaction)
    data = TransactionSerializer(transaction).data
    return render(request, 'incoming.html', {'form': form, 'data': data})


def view_record(request, pk=None):
    record = get_object_or_404(Record, pk=pk)
    transactions = Transaction.objects.filter(record=record)
    return render(
        request, 'view_record.html', {
            'record': record, 'transactions': transactions})


@group_required('Librarian')
def list_patrons(request):
    patrons = User.objects.by_group('Patron')
    return render(request, 'list_patrons.html', {'patrons': patrons})


# TODO allow self
@group_required('Librarian')
def view_patron(request, pk):
    patron = get_object_or_404(User, pk=pk)
    transactions = Transaction.objects.filter(user=patron)
    return render(
        request, 'view_patron.html', {
            'patron': patron, 'transactions': transactions})


@group_required('Librarian')
def list_transactions(request):
    transactions = Transaction.objects.all()
    return render(
        request, 'list_transactions.html', {
            'transactions': transactions})


def list_records(request):
    records = Record.objects.all()
    return render(request, 'list_records.html', {'records': records})


def list_authors(request):
    authors = Author.objects.all()
    return render(request, 'list_authors.html', {'authors': authors})


def view_author(request, slug):
    author = Author.objects.get(slug=slug)
    return render(request, 'view_author.html', {'author': author})


def view_publisher(request, slug):
    publisher = Publisher.objects.get(slug=slug)
    return render(request, 'view_publisher.html', {'publisher': publisher})


def list_publishers(request):
    objects = Publisher.objects.all()
    return render(request, 'list_publishers.html', {'objects': objects})


def index(request):
    form = LibrarySearchForm()
    return render(request, 'library_index.html', {'form': form})


def isbn_to_record(request):
    isbn = request.POST.get('isbn')
    if isbn and isbnpy.isValid(isbn):
        if isbnpy.isI10(isbn):
            isbn = isbnpy.convert(isbn)
        try:
            record = Record.objects.get(isbn13=isbn)
        except Record.DoesNotExist:
            messages.error(request, 'Book not added yet, add it first!')
            return redirect(reverse_lazy('acq') + '?isbn13=' + isbn)
        return redirect(reverse_lazy('view_record', kwargs={'pk': record.id}))
    else:
        messages.error(request, 'Invalid ISBN!')
        return redirect(reverse_lazy('library_index'))


def list_ebooks(request):
    records = Record.objects.filter(files__isnull=False).distinct()
    return render(request, 'list_records.html', {'records': records})


@group_required('Librarian')
def patron_form(request, pk=None):
    if pk:
        item = get_object_or_404(User, id=pk)
        scenario = 'Edit'
    else:
        item = User()
        scenario = 'Add'
    if request.POST:
        form = PatronForm(data=request.POST, instance=item)
        if form.is_valid():
            item = form.save(commit=False)
            item.save()
            item.set_password(form.cleaned_data['password'])
            item.save()
            if not item.add_to_group('Patron'):
                raise Exception('Add group Patron first!')
                # if request.is_ajax():
            # return render(request, 'callback.html', {'obj':
            # ItemSerializer(item).data})
            return redirect('list_patrons')
    else:
        form = PatronForm(instance=item)
        # if request.is_ajax():
    # base_template = 'modal.html'
    # else:
    # base_template = 'hr_report_base.html'
    return render(request, 'patron_form.html', {
        'scenario': scenario,
        'form': form,
        # 'base_template': base_template,
    })


def search(request, keyword=None):
    # if keyword:
    # results = SearchQuerySet().filter(content=keyword)
    if request.GET:
        form = LibrarySearchForm(data=request.GET)

    else:
        form = LibrarySearchForm()
    return render(request, 'library_search.html', {'form': form})


class RecordView(View):
    record_form = RecordForm
    book_form = BookForm
    publisher_form = PublisherForm

    rr_initial = {'key': 'value'}
    b_initial = {}
    pub_initial = {}
    record_initial_files = {}
    template_name = 'acquisition1.html'
    api_has_cover = False
    isbn = None

    @method_decorator(group_required('Librarian'))
    def dispatch(self, request, *args, **kwargs):
        if request.method == 'GET':
            if request.GET.get('isbn13'):
                self.isbn = request.GET.get('isbn13')
                if isbnpy.isValid(self.isbn):
                    if isbnpy.isI10(self.isbn):
                        self.isbn = isbnpy.convert(self.isbn)
                    response = urllib2.urlopen('https://www.googleapis.com' +
                                               '/books/v1/volumes?q=search+isbn:'
                                               +
                                               self.isbn)
                    request.session['google_api_data'] = json.load(response)
                    openlibrary_data = json.load(urllib2.urlopen(
                        'http://openlibrary.org/api/volumes/brief/json/isbn:'
                        + self.isbn))
                    if len(openlibrary_data.keys()) is not 0:
                        if 'records' in openlibrary_data[openlibrary_data.keys()[0]]:
                            if len(openlibrary_data[openlibrary_data.keys()[0]]['records'].keys()) is not 0:
                                request.session['od'] = openlibrary_data[openlibrary_data.keys()[0]]['records'][openlibrary_data[openlibrary_data.keys()[0]]['records'].keys()[0]]
        return super(RecordView, self).dispatch(request, *args, **kwargs)

    def get_objects(self, cls, *dl, **kwargs):
        if kwargs:
            return cls.objects.filter(**kwargs)
        else:
            objs = []
            for dic in dl:
                objs.append(cls.objects.get_or_create(**dic))
            return objs

    def get_from_api(self, **kwargs):
        data = kwargs['data']
        lookup_fields = kwargs['lookup_fields']
        lookup_path = kwargs['lookup_path']
        if 'form_fields' in kwargs:
            form_fields = kwargs['form_fields']
        if 'multiselect' in kwargs:
            multiselect = kwargs['multiselect']
        else:
            multiselect = False
        if 'dic_key' in kwargs:
            dic_key = kwargs['dic_key']

        for lp in lookup_path:
            if lp in data:
                data = data[lp]
            elif type(data) is list and type(lp) is int:
                data = data[lp]

        if 'cls' in kwargs:
            cls = kwargs['cls']

            if multiselect:

                for field in lookup_fields:
                    if field in data:
                        lod = []
                        if type(data[field]) is list and type(data[field][0]) is unicode:
                            values = data[field]
                            for value in values:
                                d = {}
                                d[form_fields[0]] = value
                                lod.append(d)
                            objs = self.get_objects(cls, *lod)
                            if objs:
                                ll = []
                                for o in objs:
                                    ll.append(o[0].id)
                                return ll
                        elif type(data[field]) is list and type(data[field][0]) is dict:
                            values = data[field]
                            for value in values:
                                d = {}
                                d[form_fields[0]] = value[dic_key]
                                lod.append(d)
                            objs = self.get_objects(cls, *lod)
                            if objs:
                                ll = []
                                for o in objs:
                                    ll.append(o[0].id)
                                return ll

                        elif type(data[field]) is unicode:
                            dictn = {}
                            val = data[field]
                            dictn[form_fields[0]] = val
                            objs = self.get_objects(cls, **dictn)
                            if objs:
                                ll = []
                                for o in objs:
                                    ll.append(o.id)
                                return ll

        else:
            if lookup_fields[0] in data:
                if type(data[lookup_fields[0]]) is list and len(data[lookup_fields[0]]) is not 0:
                    return data[lookup_fields[0]][0]
                elif type(data[lookup_fields[0]]) is unicode or type(data[lookup_fields[0]]) is int:
                    return data[lookup_fields[0]]
        pass

    def populate(self, google_data, ol_data):
        rr_initial_gapi = {
                           'authors': self.get_from_api(
                            data=google_data,
                            lookup_path=['items', 0, 'volumeInfo'],
                            lookup_fields=['authors'],
                            cls=Author,
                            multiselect=True,
                            form_fields=['name'],
                            ),
                           'languages': self.get_from_api(
                            data=google_data,
                            lookup_path=['items', 0, 'volumeInfo'],
                            lookup_fields=['language'],
                            cls=Language,
                            multiselect=True,
                            form_fields=['code'],
                            ),
                           'pagination': self.get_from_api(
                            data=google_data,
                            lookup_path=['items', 0, 'volumeInfo'],
                            lookup_fields=['pageCount'],
                            ),
                           'isbn13': self.isbn,
                           'date_added': timezone.now(),
                           'edition': self.get_from_api(
                            data=google_data,
                            lookup_path=['items', 0, 'volumeInfo'],
                            lookup_fields=['contentVersion']
                            ),
                           'description': self.get_from_api(
                            data=google_data,
                            lookup_path=['items', 0, 'volumeInfo'],
                            lookup_fields=['description']
                            ),
                           'date_of_publication': self.get_from_api(
                            data=google_data,
                            lookup_path=['items', 0, 'volumeInfo'],
                            lookup_fields=['publishedDate'],
                            ),
                           }
        rr_initial_olapi = {
                           'authors': self.get_from_api(
                            data=ol_data,
                            lookup_path=['details', 'details'],
                            lookup_fields=['authors'],
                            # This should be assigned when list has dict
                            dic_key='name',
                            cls=Author,
                            multiselect=True,
                            form_fields=['name'],
                            ),
                           # 'languages': self.get_from_api(
                           #  data=google_data,
                           #  lookup_path=['items', 0, 'volumeInfo'],
                           #  lookup_fields=['language'],
                           #  cls=Language,
                           #  multiselect=True,
                           #  form_fields=['code'],
                           #  ),
                           'pagination': self.get_from_api(
                            data=ol_data,
                            lookup_path=['details', 'details'],
                            lookup_fields=['pagination']
                            ),
                           'isbn13': self.isbn,
                           'date_added': timezone.now(),
                           'edition': self.get_from_api(
                            data=ol_data,
                            lookup_path=['details', 'details'],
                            lookup_fields=['edition_name']
                            ),
                           'description': self.get_from_api(
                             data=ol_data,
                             lookup_path=['details', 'details'],
                             lookup_fields=['description']
                             ),
                           'format': self.get_from_api(
                             data=ol_data,
                             lookup_path=['details', 'details'],
                             lookup_fields=['physical_format']
                             ),
                           'type': LibrarySetting.get_solo().default_type,
                           'goodreads_id': self.get_from_api(
                            data=ol_data,
                            lookup_path=['details', 'details', 'identifiers'],
                            lookup_fields=['goodreads']
                            ),
                           'librarything_id': self.get_from_api(
                            data=ol_data,
                            lookup_path=['details', 'details', 'identifiers'],
                            lookup_fields=['librarything']
                            ),
                           'openlibrary_id': self.get_from_api(
                            data=ol_data,
                            lookup_path=['data', 'identifiers'],
                            lookup_fields=['openlibrary']
                            ),
                           'lcc': self.get_from_api(
                            data=ol_data,
                            lookup_path=['details', 'details'],
                            lookup_fields=['lc_classifications']
                            ),
                           'ddc': self.get_from_api(
                            data=ol_data,
                            lookup_path=['details', 'details'],
                            lookup_fields=['dewey_decimal_class']
                            ),
                           'lccn_id': self.get_from_api(
                            data=ol_data,
                            lookup_path=['details', 'details'],
                            lookup_fields=['lccn']
                            ),
                           'oclc_id': self.get_from_api(
                            data=ol_data,
                            lookup_path=['data', 'identifiers'],
                            lookup_fields=['oclc']
                            ),
                           'dimensions': self.get_from_api(
                            data=ol_data,
                            lookup_path=['details', 'details'],
                            lookup_fields=['physical_dimensions']
                            ),
                           'by_statement': self.get_from_api(
                            data=ol_data,
                            lookup_path=['data'],
                            lookup_fields=['by_statement']
                            ),
                           'excerpt': self.get_from_api(
                            data=ol_data,
                            lookup_path=['data', 'excerpts', 0],
                            lookup_fields=['text']
                            ),
                           'published_places': self.get_from_api(
                            data=ol_data,
                            lookup_path=['details', 'details'],
                            lookup_fields=['publish_places'],
                            multiselect=True,
                            cls=Place,
                            form_fields=['name']
                            ),
                           'date_of_publication': self.to_flex_dtf(self.get_from_api(
                            data=ol_data,
                            lookup_path=['details', 'details'],
                            lookup_fields=['publish_date']
                            )),
                           'notes': self.get_from_api(
                            data=ol_data,
                            lookup_path=['data'],
                            lookup_fields=['notes']
                            ),
                           }
        b_initial_gapi = {'title': self.get_from_api(
                           data=google_data,
                           lookup_path=['items', 0, 'volumeInfo'],
                           lookup_fields=['title']
                           ),
                          'subtitle': self.get_from_api(
                           data=google_data,
                           lookup_path=['items', 0, 'volumeInfo'],
                           lookup_fields=['subtitle']
                           ),
                          # 'subjects': self.get_from_api(
                          #  data=od,
                          #  lookup_path=['details', 'details'],
                          #  lookup_fields=['subjects'],
                          #  multiselect=True,
                          #  cls=Subject,
                          #  form_fields=['name'],
                          #  ),
                          }
        b_initial_olapi = {'title': self.get_from_api(
                           data=ol_data,
                           lookup_path=['details', 'details'],
                           lookup_fields=['title']
                           ),
                           'subtitle': self.get_from_api(
                           data=ol_data,
                           lookup_path=['details', 'details'],
                           lookup_fields=['subtitle']
                           ),
                           'subjects': self.get_from_api(
                           data=ol_data,
                           lookup_path=['details', 'details'],
                           lookup_fields=['subjects'],
                           multiselect=True,
                           cls=Subject,
                           form_fields=['name'],
                           ),
                           }

        pub_initial_gapi = {'name': self.get_from_api(
                             data=google_data,
                             lookup_path=['items', 0, 'volumeInfo'],
                             lookup_fields=['publisher'],
                             ),
                            }
        pub_initial_olapi = {'name': self.get_from_api(
                             data=ol_data,
                             lookup_path=['details', 'details'],
                             lookup_fields=['publishers']
                             ),
                             }

        self.rr_initial = self.get_dict_union(rr_initial_gapi, rr_initial_olapi)
        self.b_initial = self.get_dict_union(b_initial_gapi, b_initial_olapi)
        self.pub_initial = self.get_dict_union(pub_initial_gapi, pub_initial_olapi)

        pass

    def populate_cover(self, google_data, ol_data, cover_check):
        if cover_check:
            cover_url_olapi = {
                     'small_cover': self.get_from_api(
                          data=ol_data,
                          lookup_path=['data', 'cover'],
                          lookup_fields=['small']
                         ),
                     'medium_cover': self.get_from_api(
                          data=ol_data,
                          lookup_path=['data', 'cover'],
                          lookup_fields=['medium']
                         ),
                     'large_cover': self.get_from_api(
                          data=ol_data,
                          lookup_path=['data', 'cover'],
                          lookup_fields=['large']
                         ),
                    }
            cover_url_gapi = {
                              'small_cover': self.get_from_api(
                               data=google_data,
                               lookup_path=['items', 0, 'volumeInfo', 'imageLinks'],
                               lookup_fields=['smallThumbnail']
                               ),
                              'large_cover': self.get_from_api(
                               data=google_data,
                               lookup_path=['items', 0, 'volumeInfo', 'imageLinks'],
                               lookup_fields=['thumbnail']
                               )
                             }
            cover_url = self.get_dict_union(cover_url_gapi, cover_url_olapi)
            for key in cover_url:
                if cover_url[key] is not None:
                    self.api_has_cover = True
        else:
            record_initial_files_olapi = {
                                     'small_cover': self.get_file(
                                         self.get_from_api(
                                          data=ol_data,
                                          lookup_path=['data', 'cover'],
                                          lookup_fields=['small']
                                         )),
                                     'medium_cover': self.get_file(
                                         self.get_from_api(
                                          data=ol_data,
                                          lookup_path=['data', 'cover'],
                                          lookup_fields=['medium']
                                         )),
                                     'large_cover': self.get_file(
                                         self.get_from_api(
                                          data=ol_data,
                                          lookup_path=['data', 'cover'],
                                          lookup_fields=['large']
                                         )),
                                    }
            record_initial_files_gapi = {
                                     'small_cover': self.get_file(
                                         self.get_from_api(
                                          data=google_data,
                                          lookup_path=['items', 0, 'volumeInfo', 'imageLinks'],
                                          lookup_fields=['smallThumbnail']
                                         )),
                                     'large_cover': self.get_file(
                                         self.get_from_api(
                                          data=google_data,
                                          lookup_path=['items', 0, 'volumeInfo', 'imageLinks'],
                                          lookup_fields=['thumbnail']
                                         )),
                                    }
            self.record_initial_files = self.get_dict_union(
                                        record_initial_files_gapi,
                                        record_initial_files_olapi
                                        )
        pass

    def get_file(self, url):
        if url:
            result = urllib.urlopen(url)
            fi_name = os.path.basename(url)
            suf = SimpleUploadedFile(fi_name, result.read())
            return suf
        pass

    def get_dict_union(self, dict1, dict2):
        merged_dict = {}
        dict1_keys = dict1.keys()
        dict2_keys = dict2.keys()
        keys_union = list(set(dict1_keys + dict2_keys))

        for key in keys_union:
            if key in dict1 and key not in dict2:
                merged_dict[key] = dict1[key]
            elif key in dict2 and key not in dict1:
                merged_dict[key] = dict2[key]
            elif key in dict1 and key in dict2:
                if dict1[key] is None and dict2[key] is not None:
                    merged_dict[key] = dict2[key]
                elif dict1[key] is not None and dict2[key] is None:
                    merged_dict[key] = dict1[key]
                elif dict1[key] is not None and dict2[key] is not None:
                    merged_dict[key] = dict2[key]
        return merged_dict

    def get(self, request, *args, **kwargs):
        if request.GET.get('isbn13'):
            google_data = request.session.get('google_api_data', {})
            ol_data = request.session.get('od', {})
            self.populate(google_data, ol_data)
            self.populate_cover(google_data, ol_data, True)

        if 'record_id' in self.kwargs:
            rec_id = int(self.kwargs['record_id'])
            record_instance = Record.objects.get(id=rec_id)
            rr_form = self.record_form(instance=record_instance)
            book_instance = Book.objects.get(id=record_instance.book.id)
            b_form = self.book_form(instance=book_instance)
            if record_instance.publisher:
                publisher_instance = Publisher.objects.get(id=record_instance.publisher.id)
                pub_form = self.publisher_form(instance=publisher_instance)
            else:
                pub_form = self.publisher_form()
        else:
            rr_form = self.record_form(initial=self.rr_initial)
            b_form = self.book_form(initial=self.b_initial)
            pub_form = self.publisher_form(initial=self.pub_initial)

        context = {'rr_form': rr_form,
                   'b_form': b_form,
                   'pub_form': pub_form,
                   'api_has_cover': self.api_has_cover,
                   'record_id': self.kwargs.get('record_id', None),
                   }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        post_data = request.POST.copy()
        mixd_selectize_fields = {'subjects': [Subject, 'name'],
                                 'authors': [Author, 'name'],
                                 'published_places': [Place, 'name']
                                 }
        post_data = self.fix_mixds_data(post_data, mixd_selectize_fields)

        book_fields = {'title': False, 'subtitle': False, 'subjects': True}
        publisher_fields = {'name': False}
        post_data = self.change_post_data(Book, book_fields, post_data, 'book')
        post_data = self.change_post_data(Publisher, publisher_fields, post_data, 'publisher')

        if 'record_id' in self.kwargs:
            rec_id = int(self.kwargs['record_id'])
            instance = Record.objects.get(id=rec_id)
            record = RecordForm(post_data, request.FILES, instance=instance)
        else:
            files_from_api = {}
            files_from_request = request.FILES
            google_data = request.session.get('google_api_data', {})
            ol_data = request.session.get('od', {})
            self.populate_cover(google_data, ol_data, False)
            for key in self.record_initial_files:
                if self.record_initial_files[key] is not None:
                    files_from_api[key] = self.record_initial_files[key]
            # Later dictionary will be of high priority in conflict during merge.
            files_combo = dict(files_from_api.items() + files_from_request.items())
            record = RecordForm(post_data, files_combo)

        if record.is_valid():
            record.save()
        else:
            rr_form = self.record_form(post_data, request.FILES)
            b_form = self.book_form(post_data)
            pub_form = self.publisher_form(post_data)
            context = {'rr_form': rr_form,
                       'b_form': b_form,
                       'pub_form': pub_form,
                       'api_has_cover': self.api_has_cover,
                       'record_id': self.kwargs.get('record_id', None),
                       }
            return render(request, self.template_name, context)
        if 'google_api_data' in request.session:
            del request.session['google_api_data']
        if 'od' in request.session:
            del request.session['od']
        return HttpResponseRedirect('/library/records/')

    def change_post_data(self, cls, fields, data, field_to_alter):
        value = {}
        dictionary = {}
        for field in fields:
            value[field] = data.getlist(field, None)
        for f_field, v in zip(fields, value):
            if value[f_field] is not None and len(value[f_field][0]) is not 0:
                if fields[f_field]:
                    for i, val in enumerate(value[f_field]):
                        value[f_field][i] = int(value[f_field][i])
                    dictionary[f_field] = value[f_field]
                else:
                    dictionary[f_field] = value[f_field][0]

        obj = self.m2m_filter(cls, dictionary)
        if len(obj) is not 0:
            alter_value = unicode(obj[0].id)
        else:
            alter_value = self.m2m_create(cls, dictionary)
            # alter_value = unicode(obj.id)
        data.__setitem__(field_to_alter, alter_value)
        return data
        pass

    def m2m_filter(self, cls, data):
        if len(data) is not 0:
            filtrd = cls.objects.filter()
            for key in data:
                if type(data[key]) is not list:
                    df = {}
                    df[key] = data[key]
                    filtrd = filtrd.filter(**df)
                else:
                    # for item in data[key]:
                    df = {}
                    u_key = key + '__in'
                    df[u_key] = data[key]
                    filtrd = filtrd.filter(**df).distinct()
            return filtrd
        else:
            return []

    def m2m_create(self, klass, dictionary):
        if len(dictionary) is not 0:
            obj = klass()

            # set regular fields
            for field, value in dictionary.iteritems():
                if not isinstance(value, list):
                    setattr(obj, field, value)

            obj.save()

            # set M2M fields
            for field, value in dictionary.iteritems():
                if isinstance(value, list):
                    setattr(obj, field, value)

            return obj.id
        else:
            return u''

    def fix_mixds_data(self, data, mxdfields):
        ripped_dict = {}
        for key in mxdfields:
            if key in data:
                ripped_dict[key] = data.getlist(key, None)
        for key in ripped_dict:
            value = ripped_dict[key]
            for i, val in enumerate(value):
                if not re.match(r'^[0-9]+$', val):
                    d = {}
                    d[mxdfields[key][1]] = val
                    obj = mxdfields[key][0].objects.create(**d)
                    value[i] = unicode(obj.id)
            ripped_dict[key] = value
        for key in ripped_dict:
            data.setlist(key, ripped_dict[key])
        return data

    @staticmethod
    def to_flex_dtf(string):
        if string is not None:
            try:
                return datetime.datetime.strptime(string, "%B %d, %Y").strftime('%Y-%m-%d')
            except ValueError:
                try:
                    return datetime.datetime.strptime(string, "%B %Y").strftime('%Y-%m')
                except ValueError:
                    return string
        else:
            return string


