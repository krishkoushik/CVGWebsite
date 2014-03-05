# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Video.name'
        db.alter_column(u'website_video', 'name', self.gf('django.db.models.fields.CharField')(default='', max_length=100))

    def backwards(self, orm):

        # Changing field 'Video.name'
        db.alter_column(u'website_video', 'name', self.gf('django.db.models.fields.CharField')(max_length=100, null=True))

    models = {
        u'website.photo': {
            'Meta': {'object_name': 'Photo'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        u'website.project': {
            'Meta': {'object_name': 'Project'},
            'brief': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'detail': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imag': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'aux'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['website.Photo']"}),
            'main_imag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'main'", 'to': u"orm['website.Photo']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'videos': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['website.Video']", 'null': 'True', 'blank': 'True'})
        },
        u'website.video': {
            'Meta': {'object_name': 'Video'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'video': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['website']