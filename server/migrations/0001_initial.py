# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Conference'
        db.create_table('conferences', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('unique_name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('year', self.gf('django.db.models.fields.IntegerField')()),
            ('month', self.gf('django.db.models.fields.IntegerField')()),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('server', ['Conference'])

        # Adding model 'User'
        db.create_table('users', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('f_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('l_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=500)),
        ))
        db.send_create_signal('server', ['User'])

        # Adding model 'Registration'
        db.create_table('registrations', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['server.User'])),
            ('conference', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['server.Conference'])),
        ))
        db.send_create_signal('server', ['Registration'])

        # Adding model 'Likes'
        db.create_table('likes', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('registration_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['server.Registration'])),
            ('likes', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('server', ['Likes'])

        # Adding model 'Logs'
        db.create_table('logs', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('registration_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['server.Registration'])),
            ('action', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('data', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('server', ['Logs'])


    def backwards(self, orm):
        # Deleting model 'Conference'
        db.delete_table('conferences')

        # Deleting model 'User'
        db.delete_table('users')

        # Deleting model 'Registration'
        db.delete_table('registrations')

        # Deleting model 'Likes'
        db.delete_table('likes')

        # Deleting model 'Logs'
        db.delete_table('logs')


    models = {
        'server.conference': {
            'Meta': {'object_name': 'Conference', 'db_table': "'conferences'"},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'month': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'unique_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'year': ('django.db.models.fields.IntegerField', [], {})
        },
        'server.likes': {
            'Meta': {'object_name': 'Likes', 'db_table': "'likes'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'likes': ('django.db.models.fields.TextField', [], {}),
            'registration_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['server.Registration']"})
        },
        'server.logs': {
            'Meta': {'object_name': 'Logs', 'db_table': "'logs'"},
            'action': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'data': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'registration_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['server.Registration']"})
        },
        'server.registration': {
            'Meta': {'object_name': 'Registration', 'db_table': "'registrations'"},
            'conference': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['server.Conference']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['server.User']"})
        },
        'server.user': {
            'Meta': {'object_name': 'User', 'db_table': "'users'"},
            'email': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'f_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'l_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        }
    }

    complete_apps = ['server']