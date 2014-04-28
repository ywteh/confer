# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding unique constraint on 'AList', fields ['user_starred', 'user', 'registration']
        db.create_unique('alist', ['user_starred_id', 'user_id', 'registration_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'AList', fields ['user_starred', 'user', 'registration']
        db.delete_unique('alist', ['user_starred_id', 'user_id', 'registration_id'])


    models = {
        'server.alist': {
            'Meta': {'unique_together': "(('registration', 'user', 'user_starred'),)", 'object_name': 'AList', 'db_table': "'alist'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'registration': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['server.Registration']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user'", 'to': "orm['server.User']"}),
            'user_starred': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_starred'", 'to': "orm['server.User']"})
        },
        'server.app': {
            'Meta': {'object_name': 'App', 'db_table': "'apps'"},
            'app_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'app_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'app_token': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['server.User']"})
        },
        'server.conference': {
            'Meta': {'ordering': "['-start_date']", 'object_name': 'Conference', 'db_table': "'conferences'"},
            'admins': ('django.db.models.fields.TextField', [], {'default': "'[]'"}),
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
        'server.following': {
            'Meta': {'unique_together': "(('paper_id', 'conference', 'user'),)", 'object_name': 'Following', 'db_table': "'following'"},
            'conference': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['server.Conference']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'paper_id': ('django.db.models.fields.TextField', [], {}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['server.User']"})
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
        'server.permission': {
            'Meta': {'object_name': 'Permission', 'db_table': "'permissions'"},
            'access': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'app': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['server.App']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['server.User']"})
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