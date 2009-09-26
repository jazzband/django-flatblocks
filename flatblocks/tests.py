import unittest

from django import template
from django.test import TestCase
from django.core.cache import cache
from django.contrib.auth.models import User
from django import db

from flatblocks import models
from flatblocks.settings import CACHE_PREFIX


class BasicTests(TestCase):
    urls = 'flatblocks.urls'

    def setUp(self):
        self.testblock = models.FlatBlock()
        self.testblock.slug = 'block'
        self.testblock.header = 'HEADER'
        self.testblock.content = 'CONTENT'
        self.testblock.save()
        self.admin = User.objects.create_superuser('admin', 'admin@localhost', 'adminpwd')
    
    def testURLConf(self):
        self.assertEquals(self.client.get('/edit/1/').template.name, 'admin/login.html')
        self.client.login(username='admin', password='adminpwd')
        self.assertEquals(self.client.get('/edit/1/').template.name, 'flatblocks/edit.html')

    def testCacheReset(self):
        """
        Tests if FlatBlock.save() resets the cache.
        """
        tpl = template.Template('{% load flatblock_tags %}{% flatblock "block" 60 %}')
        tpl.render({})
        name = '%sblock' % CACHE_PREFIX
        self.assertNotEquals(None, cache.get(name))
        block = models.FlatBlock.objects.get(slug='block')
        block.header = 'UPDATED'
        block.save()
        self.assertEquals(None, cache.get(name))
        
    def testSaveKwargs(self):
        block = models.FlatBlock()
        block.slug = 'missing'
        self.assertRaises(ValueError, block.save, force_update=True)
        block = models.FlatBlock.objects.get(slug='block')
        self.assertRaises(db.IntegrityError, block.save, force_insert=True)

    def tearDown(self):
        self.testblock.delete()

class TagTests(unittest.TestCase):
    def setUp(self):
        self.testblock = models.FlatBlock()
        self.testblock.slug = 'block'
        self.testblock.header = 'HEADER'
        self.testblock.content = 'CONTENT'
        self.testblock.save()

    def testLoadingTaglib(self):
        """Tests if the taglib defined in this app can be loaded"""
        tpl = template.Template('{% load flatblock_tags %}')
        tpl.render({})

    def testMissingBlock(self):
        """Tests if a missing block will simply return an empty string"""
        tpl = template.Template('{% load flatblock_tags %}{% flatblock "missing_block" %}')
        self.assertEqual('', tpl.render({}).strip())

    def testExistingPlain(self):
        tpl = template.Template('{% load flatblock_tags %}{% plain_flatblock "block" %}')
        self.assertEqual(u'CONTENT', tpl.render({}).strip()) 

    def testExistingTemplate(self):
        expected = """<div class="flatblock block-block">
    
    <h2 class="title">HEADER</h2>
    
    <div class="content">CONTENT</div>
</div>"""
        tpl = template.Template('{% load flatblock_tags %}{% flatblock "block" %}')
        self.assertEqual(expected, tpl.render({}))

    def testUsingMissingTemplate(self):
        tpl = template.Template('{% load flatblock_tags %}{% flatblock "block" using "missing_template.html" %}')
        exception = template.TemplateDoesNotExist
        self.assertRaises(exception, tpl.render, {})

    def testSyntax(self):
        tpl = template.Template('{% load flatblock_tags %}{% flatblock "block" %}')
        tpl.render({})
        tpl = template.Template('{% load flatblock_tags %}{% flatblock "block" 123 %}')
        tpl.render({})
        tpl = template.Template('{% load flatblock_tags %}{% flatblock "block" using "flatblocks/flatblock.html" %}')
        tpl.render({})
        tpl = template.Template('{% load flatblock_tags %}{% flatblock "block" 123 using "flatblocks/flatblock.html" %}')
        tpl.render({})

    def testBlockAsVariable(self):
        tpl = template.Template('{% load flatblock_tags %}{% flatblock blockvar %}')
        tpl.render({'blockvar': 'block'})

    def tearDown(self):
        self.testblock.delete()

class ModelTestCase(unittest.TestCase):
    """A selection of testcases regarding the models themselves"""
    pass

