# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Apps'
        db.create_table('apps', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('app_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('app_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('app_token', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['server.User'])),
        ))
        db.send_create_signal('server', ['Apps'])


    def backwards(self, orm):
        # Deleting model 'Apps'
        db.delete_table('apps')


    models = {
        'server.apps': {
            'Meta': {'object_name': 'Apps', 'db_table': "'apps'"},
            'app_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'app_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'app_token': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['server.User']"})
        },
        'server.conference': {
            'Meta': {'ordering': "['-start_date']", 'object_name': 'Conference', 'db_table': "'conferences'"},
            'blurb': ('django.db.models.fields.TextField', [], {}),
            'confer_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'end_date': ('django.db.models.fields.DateField', [], {}),
            'hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'start_date': ('django.db.models.fields.DateField', [], {}),
            'subtitle': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.TextField', [], {}),
            'unique_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
        'server.likes': {
            'Meta': {'object_name': 'Likes', 'db_table': "'likes'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'likes': ('django.db.models.fields.TextField', [], {}),
            'registration': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['server.Registration']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'server.logs': {
            'Meta': {'ordering': "['-timestamp']", 'object_name': 'Logs', 'db_table': "'logs'"},
            'action': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'data': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'registration': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['server.Registration']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'server.registration': {
            'Meta': {'object_name': 'Registration', 'db_table': "'registrations'"},
            'conference': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['server.Conference']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['server.User']"})
        },
        'server.user': {
            'Meta': {'object_name': 'User', 'db_table': "'users'"},
            'email': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'f_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'l_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'meetups_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['server']