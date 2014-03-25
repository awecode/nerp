# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Subject'
        db.create_table(u'ils_subject', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=254, null=True, blank=True)),
            ('parent', self.gf('mptt.fields.TreeForeignKey')(blank=True, related_name='children', null=True, to=orm['ils.Subject'])),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=255, blank=True)),
            (u'lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal(u'ils', ['Subject'])

        # Adding model 'Author'
        db.create_table(u'ils_author', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=255, blank=True)),
        ))
        db.send_create_signal(u'ils', ['Author'])

        # Adding model 'Book'
        db.create_table(u'ils_book', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=254)),
            ('subtitle', self.gf('django.db.models.fields.CharField')(max_length=254, null=True, blank=True)),
            ('language', self.gf('django.db.models.fields.CharField')(default='en', max_length=7, null=True, blank=True)),
            ('subject', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ils.Subject'])),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=255, blank=True)),
        ))
        db.send_create_signal(u'ils', ['Book'])

        # Adding M2M table for field authors on 'Book'
        m2m_table_name = db.shorten_name(u'ils_book_authors')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('book', models.ForeignKey(orm[u'ils.book'], null=False)),
            ('author', models.ForeignKey(orm[u'ils.author'], null=False))
        ))
        db.create_unique(m2m_table_name, ['book_id', 'author_id'])

        # Adding model 'Record'
        db.create_table(u'ils_record', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('edition', self.gf('django.db.models.fields.CharField')(max_length=254, null=True, blank=True)),
            ('format', self.gf('django.db.models.fields.CharField')(max_length=254, null=True, blank=True)),
            ('pagination', self.gf('django.db.models.fields.CharField')(max_length=254, null=True, blank=True)),
            ('isbn13', self.gf('django.db.models.fields.CharField')(max_length=254, null=True, blank=True)),
            ('date_of_publication', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('price', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('quantity', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('type', self.gf('django.db.models.fields.IntegerField')(unique=True)),
            ('book', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ils.Book'])),
        ))
        db.send_create_signal(u'ils', ['Record'])

        # Adding model 'Transaction'
        db.create_table(u'ils_transaction', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('record', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ils.Record'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.User'])),
            ('borrow_date', self.gf('django.db.models.fields.DateField')()),
            ('due_date', self.gf('django.db.models.fields.DateField')()),
            ('return_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('returned', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('fine_per_day', self.gf('django.db.models.fields.FloatField')()),
            ('fine_paid', self.gf('django.db.models.fields.FloatField')(default=False)),
        ))
        db.send_create_signal(u'ils', ['Transaction'])

        # Adding model 'LibrarySetting'
        db.create_table(u'ils_librarysetting', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fine_per_day', self.gf('django.db.models.fields.FloatField')()),
            ('borrow_days', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'ils', ['LibrarySetting'])


    def backwards(self, orm):
        # Deleting model 'Subject'
        db.delete_table(u'ils_subject')

        # Deleting model 'Author'
        db.delete_table(u'ils_author')

        # Deleting model 'Book'
        db.delete_table(u'ils_book')

        # Removing M2M table for field authors on 'Book'
        db.delete_table(db.shorten_name(u'ils_book_authors'))

        # Deleting model 'Record'
        db.delete_table(u'ils_record')

        # Deleting model 'Transaction'
        db.delete_table(u'ils_transaction')

        # Deleting model 'LibrarySetting'
        db.delete_table(u'ils_librarysetting')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'ils.author': {
            'Meta': {'object_name': 'Author'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'blank': 'True'})
        },
        u'ils.book': {
            'Meta': {'object_name': 'Book'},
            'authors': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['ils.Author']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'en'", 'max_length': '7', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'blank': 'True'}),
            'subject': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ils.Subject']"}),
            'subtitle': ('django.db.models.fields.CharField', [], {'max_length': '254', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '254'})
        },
        u'ils.librarysetting': {
            'Meta': {'object_name': 'LibrarySetting'},
            'borrow_days': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'fine_per_day': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'ils.record': {
            'Meta': {'object_name': 'Record'},
            'book': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ils.Book']"}),
            'date_of_publication': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'edition': ('django.db.models.fields.CharField', [], {'max_length': '254', 'null': 'True', 'blank': 'True'}),
            'format': ('django.db.models.fields.CharField', [], {'max_length': '254', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isbn13': ('django.db.models.fields.CharField', [], {'max_length': '254', 'null': 'True', 'blank': 'True'}),
            'pagination': ('django.db.models.fields.CharField', [], {'max_length': '254', 'null': 'True', 'blank': 'True'}),
            'price': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'quantity': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'type': ('django.db.models.fields.IntegerField', [], {'unique': 'True'})
        },
        u'ils.subject': {
            'Meta': {'object_name': 'Subject'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '254', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['ils.Subject']"}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'blank': 'True'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        u'ils.transaction': {
            'Meta': {'object_name': 'Transaction'},
            'borrow_date': ('django.db.models.fields.DateField', [], {}),
            'due_date': ('django.db.models.fields.DateField', [], {}),
            'fine_paid': ('django.db.models.fields.FloatField', [], {'default': 'False'}),
            'fine_per_day': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'record': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ils.Record']"}),
            'return_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'returned': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.User']"})
        },
        u'users.user': {
            'Meta': {'object_name': 'User'},
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '254', 'db_index': 'True'}),
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '245'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'users'", 'symmetrical': 'False', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        }
    }

    complete_apps = ['ils']