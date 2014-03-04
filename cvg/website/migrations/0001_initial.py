# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Photo'
        db.create_table(u'website_photo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal(u'website', ['Photo'])

        # Adding model 'Video'
        db.create_table(u'website_video', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('video', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal(u'website', ['Video'])

        # Adding model 'Project'
        db.create_table(u'website_project', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('brief', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('detail', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('main_imag', self.gf('django.db.models.fields.related.ForeignKey')(related_name='main', to=orm['website.Photo'])),
            ('date', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal(u'website', ['Project'])

        # Adding M2M table for field imag on 'Project'
        m2m_table_name = db.shorten_name(u'website_project_imag')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('project', models.ForeignKey(orm[u'website.project'], null=False)),
            ('photo', models.ForeignKey(orm[u'website.photo'], null=False))
        ))
        db.create_unique(m2m_table_name, ['project_id', 'photo_id'])

        # Adding M2M table for field videos on 'Project'
        m2m_table_name = db.shorten_name(u'website_project_videos')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('project', models.ForeignKey(orm[u'website.project'], null=False)),
            ('video', models.ForeignKey(orm[u'website.video'], null=False))
        ))
        db.create_unique(m2m_table_name, ['project_id', 'video_id'])


    def backwards(self, orm):
        # Deleting model 'Photo'
        db.delete_table(u'website_photo')

        # Deleting model 'Video'
        db.delete_table(u'website_video')

        # Deleting model 'Project'
        db.delete_table(u'website_project')

        # Removing M2M table for field imag on 'Project'
        db.delete_table(db.shorten_name(u'website_project_imag'))

        # Removing M2M table for field videos on 'Project'
        db.delete_table(db.shorten_name(u'website_project_videos'))


    models = {
        u'website.photo': {
            'Meta': {'object_name': 'Photo'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'video': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['website']