# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FlatBlock',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.CharField(help_text='A unique name used for reference in the templates', unique=True, max_length=255, verbose_name='Slug')),
                ('header', models.CharField(help_text='An optional header for this content', max_length=255, verbose_name='Header', blank=True)),
                ('content', models.TextField(verbose_name='Content', blank=True)),
            ],
            options={
                'verbose_name': 'Flat block',
                'verbose_name_plural': 'Flat blocks',
            },
            bases=(models.Model,),
        ),
    ]
