# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'FlatBlock', fields ['slug']
        db.delete_unique(u'flatblocks_flatblock', ['slug'])

        # Adding M2M table for field sites on 'FlatBlock'
        m2m_table_name = db.shorten_name(u'flatblocks_flatblock_sites')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('flatblock', models.ForeignKey(orm[u'flatblocks.flatblock'], null=False)),
            ('site', models.ForeignKey(orm[u'sites.site'], null=False))
        ))
        db.create_unique(m2m_table_name, ['flatblock_id', 'site_id'])


        # Changing field 'FlatBlock.content'
        db.alter_column(u'flatblocks_flatblock', 'content', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'FlatBlock.header'
        db.alter_column(u'flatblocks_flatblock', 'header', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

    def backwards(self, orm):
        # Removing M2M table for field sites on 'FlatBlock'
        db.delete_table(db.shorten_name(u'flatblocks_flatblock_sites'))


        # Changing field 'FlatBlock.content'
        db.alter_column(u'flatblocks_flatblock', 'content', self.gf('django.db.models.fields.TextField')(default=''))

        # Changing field 'FlatBlock.header'
        db.alter_column(u'flatblocks_flatblock', 'header', self.gf('django.db.models.fields.CharField')(default='', max_length=255))
        # Adding unique constraint on 'FlatBlock', fields ['slug']
        db.create_unique(u'flatblocks_flatblock', ['slug'])


    models = {
        u'flatblocks.flatblock': {
            'Meta': {'object_name': 'FlatBlock'},
            'content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'header': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['sites.Site']", 'symmetrical': 'False'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['flatblocks']