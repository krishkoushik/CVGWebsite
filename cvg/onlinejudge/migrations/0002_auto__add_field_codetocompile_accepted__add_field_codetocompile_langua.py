# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'CodeToCompile.accepted'
        db.add_column(u'onlinejudge_codetocompile', 'accepted',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'CodeToCompile.language'
        db.add_column(u'onlinejudge_codetocompile', 'language',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)


        # Changing field 'CodeToCompile.time_of_submission'
        db.alter_column(u'onlinejudge_codetocompile', 'time_of_submission', self.gf('django.db.models.fields.IntegerField')(null=True))
        # Deleting field 'Problem.compile_line'
        db.delete_column(u'onlinejudge_problem', 'compile_line')

        # Adding field 'Problem.arguements'
        db.add_column(u'onlinejudge_problem', 'arguements',
                      self.gf('django.db.models.fields.CharField')(default='hello', max_length=300),
                      keep_default=False)

        # Adding field 'Problem.time_limit'
        db.add_column(u'onlinejudge_problem', 'time_limit',
                      self.gf('django.db.models.fields.IntegerField')(default=3000),
                      keep_default=False)

        # Adding field 'Problem.mem_limit'
        db.add_column(u'onlinejudge_problem', 'mem_limit',
                      self.gf('django.db.models.fields.IntegerField')(default=1000000000),
                      keep_default=False)

        # Adding field 'Problem.disk_limit'
        db.add_column(u'onlinejudge_problem', 'disk_limit',
                      self.gf('django.db.models.fields.IntegerField')(default=100000000),
                      keep_default=False)

        # Adding field 'Problem.check_script'
        db.add_column(u'onlinejudge_problem', 'check_script',
                      self.gf('django.db.models.fields.CharField')(default='script.sh', max_length=100),
                      keep_default=False)

        # Adding field 'Problem.prob_dir'
        db.add_column(u'onlinejudge_problem', 'prob_dir',
                      self.gf('django.db.models.fields.CharField')(default='gen', max_length=100),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'CodeToCompile.accepted'
        db.delete_column(u'onlinejudge_codetocompile', 'accepted')

        # Deleting field 'CodeToCompile.language'
        db.delete_column(u'onlinejudge_codetocompile', 'language')


        # Changing field 'CodeToCompile.time_of_submission'
        db.alter_column(u'onlinejudge_codetocompile', 'time_of_submission', self.gf('django.db.models.fields.IntegerField')(default=1))
        # Adding field 'Problem.compile_line'
        db.add_column(u'onlinejudge_problem', 'compile_line',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=300),
                      keep_default=False)

        # Deleting field 'Problem.arguements'
        db.delete_column(u'onlinejudge_problem', 'arguements')

        # Deleting field 'Problem.time_limit'
        db.delete_column(u'onlinejudge_problem', 'time_limit')

        # Deleting field 'Problem.mem_limit'
        db.delete_column(u'onlinejudge_problem', 'mem_limit')

        # Deleting field 'Problem.disk_limit'
        db.delete_column(u'onlinejudge_problem', 'disk_limit')

        # Deleting field 'Problem.check_script'
        db.delete_column(u'onlinejudge_problem', 'check_script')

        # Deleting field 'Problem.prob_dir'
        db.delete_column(u'onlinejudge_problem', 'prob_dir')


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
            'accepted': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'compilemessage': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'compileoutp': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'fil_e': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'problemid': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['onlinejudge.Problem']"}),
            'processed': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'runtimemessage': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'runtimeoutp': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'time_of_submission': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
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
            'arguements': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'check_script': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'contest': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['onlinejudge.Contest']"}),
            'disk_limit': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mem_limit': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'prob_dir': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'statement': ('ckeditor.fields.RichTextField', [], {}),
            'time_limit': ('django.db.models.fields.IntegerField', [], {})
        },
        u'onlinejudge.requestqueue': {
            'Meta': {'object_name': 'RequestQueue'},
            'codetocompile': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['onlinejudge.CodeToCompile']", 'unique': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['onlinejudge']