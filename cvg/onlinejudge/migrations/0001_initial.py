# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Contest'
        db.create_table(u'onlinejudge_contest', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('time', self.gf('django.db.models.fields.IntegerField')()),
            ('start_time', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'onlinejudge', ['Contest'])

        # Adding model 'CurrentContest'
        db.create_table(u'onlinejudge_currentcontest', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('contest', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['onlinejudge.Contest'])),
        ))
        db.send_create_signal(u'onlinejudge', ['CurrentContest'])

        # Adding model 'Problem'
        db.create_table(u'onlinejudge_problem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('statement', self.gf('ckeditor.fields.RichTextField')()),
            ('compile_line', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('contest', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['onlinejudge.Contest'])),
        ))
        db.send_create_signal(u'onlinejudge', ['Problem'])

        # Adding model 'CodeToCompile'
        db.create_table(u'onlinejudge_codetocompile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('fil_e', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('compileoutp', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('runtimeoutp', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('compilemessage', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('runtimemessage', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('problemid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['onlinejudge.Problem'])),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('processed', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('time_of_submission', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'onlinejudge', ['CodeToCompile'])

        # Adding model 'RequestQueue'
        db.create_table(u'onlinejudge_requestqueue', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('codetocompile', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['onlinejudge.CodeToCompile'], unique=True)),
        ))
        db.send_create_signal(u'onlinejudge', ['RequestQueue'])


    def backwards(self, orm):
        # Deleting model 'Contest'
        db.delete_table(u'onlinejudge_contest')

        # Deleting model 'CurrentContest'
        db.delete_table(u'onlinejudge_currentcontest')

        # Deleting model 'Problem'
        db.delete_table(u'onlinejudge_problem')

        # Deleting model 'CodeToCompile'
        db.delete_table(u'onlinejudge_codetocompile')

        # Deleting model 'RequestQueue'
        db.delete_table(u'onlinejudge_requestqueue')


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
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'onlinejudge.codetocompile': {
            'Meta': {'object_name': 'CodeToCompile'},
            'compilemessage': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'compileoutp': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'fil_e': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'problemid': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['onlinejudge.Problem']"}),
            'processed': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'runtimemessage': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'runtimeoutp': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'time_of_submission': ('django.db.models.fields.IntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'onlinejudge.contest': {
            'Meta': {'object_name': 'Contest'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'start_time': ('django.db.models.fields.IntegerField', [], {}),
            'time': ('django.db.models.fields.IntegerField', [], {})
        },
        u'onlinejudge.currentcontest': {
            'Meta': {'object_name': 'CurrentContest'},
            'contest': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['onlinejudge.Contest']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'onlinejudge.problem': {
            'Meta': {'object_name': 'Problem'},
            'compile_line': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'contest': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['onlinejudge.Contest']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'statement': ('ckeditor.fields.RichTextField', [], {})
        },
        u'onlinejudge.requestqueue': {
            'Meta': {'object_name': 'RequestQueue'},
            'codetocompile': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['onlinejudge.CodeToCompile']", 'unique': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['onlinejudge']