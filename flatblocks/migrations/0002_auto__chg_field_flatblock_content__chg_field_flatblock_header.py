# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'FlatBlock.content'
        db.alter_column(u'flatblocks_flatblock', 'content', self.gf('django.db.models.fields.TextField')(default=''))

        # Changing field 'FlatBlock.header'
        db.alter_column(u'flatblocks_flatblock', 'header', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

    def backwards(self, orm):

        # Changing field 'FlatBlock.content'
        db.alter_column(u'flatblocks_flatblock', 'content', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'FlatBlock.header'
        db.alter_column(u'flatblocks_flatblock', 'header', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

    models = {
        u'flatblocks.flatblock': {
            'Meta': {'object_name': 'FlatBlock'},
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'header': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        }
    }

    complete_apps = ['flatblocks']