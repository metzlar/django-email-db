# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Message'
        db.create_table(u'django_email_db_message', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('body', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('from_email', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('to', self.gf('django.db.models.fields.TextField')()),
            ('bcc', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('cc', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('headers', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('unknown_attrs', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('sent', self.gf('django.db.models.fields.DateTimeField')(null=True)),
        ))
        db.send_create_signal(u'django_email_db', ['Message'])

        # Adding model 'MessageAttachment'
        db.create_table(u'django_email_db_messageattachment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('message', self.gf('django.db.models.fields.related.ForeignKey')(related_name='attachments', to=orm['django_email_db.Message'])),
            ('headers', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('document', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal(u'django_email_db', ['MessageAttachment'])


    def backwards(self, orm):
        # Deleting model 'Message'
        db.delete_table(u'django_email_db_message')

        # Deleting model 'MessageAttachment'
        db.delete_table(u'django_email_db_messageattachment')


    models = {
        u'django_email_db.message': {
            'Meta': {'object_name': 'Message'},
            'bcc': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'body': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'cc': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'from_email': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'headers': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sent': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'to': ('django.db.models.fields.TextField', [], {}),
            'unknown_attrs': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'django_email_db.messageattachment': {
            'Meta': {'object_name': 'MessageAttachment'},
            'document': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'headers': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'attachments'", 'to': u"orm['django_email_db.Message']"})
        }
    }

    complete_apps = ['django_email_db']