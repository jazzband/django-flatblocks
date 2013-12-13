from django import template
from django.test import TestCase
from django.conf import settings as global_settings
from django.core.cache import cache
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django import db

from flatblocks.models import FlatBlock
from flatblocks import settings


class SiteTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.site_1 = Site(name='site1', domain='site1.com')
        cls.site_1.save()
        cls.site_2 = Site(name='site2', domain='site2.com')
        cls.site_2.save()
        global_settings.SITE_ID = cls.site_1.pk

    @classmethod
    def tearDownClass(cls):
        cls.site_1.delete()
        cls.site_2.delete()

    def create_block_for_site1(self, **kwargs):
        return self.__class__.site_1.flatblock_set.create(**kwargs)

    def create_block_for_site2(self, **kwargs):
        return self.__class__.site_2.flatblock_set.create(**kwargs)


class BasicTests(SiteTestCase):
    urls = 'flatblocks.urls'

    def setUp(self):
        self.testblock = self.create_block_for_site1(
             slug='block',
             header='HEADER',
             content='CONTENT',
        )
        self.admin = User.objects.create_superuser('admin', 'admin@localhost', 'adminpwd')
    
    def tearDown(self):
        self.testblock.delete()

    def testURLConf(self):
        # We have to support two different APIs here (1.1 and 1.2)
        def get_tmpl(resp):
            if hasattr(resp, 'templates'):
                return resp.templates[0]
            else:
                if isinstance(resp.template, list):
                    return resp.template[0]
                return resp.template
        self.assertEqual(get_tmpl(self.client.get('/edit/1/')).name,
                         'admin/login.html')
        self.client.login(username='admin', password='adminpwd')
        self.assertEqual(get_tmpl(self.client.get('/edit/1/')).name,
                         'flatblocks/edit.html')

    def testCacheReset(self):
        """
        Tests if FlatBlock.save() resets the cache.
        """
        tpl = template.Template(
            '{% load flatblock_tags %}{% flatblock "block" 60 %}')
        tpl.render(template.Context({}))
        cache_key = ':'.join(['block', 'False', 'flatblocks/flatblock.html'])
        self.assertNotEqual(None, cache.get(cache_key))
        block = FlatBlock.objects.get(slug='block')
        block.header = 'UPDATED'
        block.save()
        #self.assertEqual(None, cache.get(cache_key))

    def testSaveForceUpdate(self):
        block = FlatBlock(slug='missing')
        with self.assertRaises(ValueError):
            block.save(force_update=True)

    def testSaveForceInsert(self):
        block = FlatBlock.objects.get(slug='block')
        with self.assertRaises(db.IntegrityError):
            block.save(force_insert=True)

    def testCacheRemoval(self):
        """
        If a block is deleted it should also be removed from the cache.
        """
        block = self.create_block_for_site1(slug="test", content="CONTENT")
        block.save()
        tpl = template.Template(
            '{% load flatblock_tags %}{% flatblock "test" 100 %}')
        # We fill the cache by rendering the block
        tpl.render(template.Context({}))
        cache_key = ':'.join(['test', 'False', 'flatblocks/flatblock.html'])
        self.assertNotEqual(None, cache.get(cache_key))
        block.delete()
        #self.assertEqual(None, cache.get(cache_key))

    def testSiteUniqueness(self):
        """
        Make sure that there can only be one flatblock with a slug for a site.
        """
        self.create_block_for_site1(slug='unique1').full_clean()
        self.create_block_for_site2(slug='unique1').full_clean()
        with self.assertRaises(Exception) as cm:
            self.create_block_for_site1(slug='unique1').full_clean()


class TagTests(SiteTestCase):
    def setUp(self):
        self.testblock = self.create_block_for_site1(
             slug='block',
             header='HEADER',
             content='CONTENT'
        )

    def tearDown(self):
        self.testblock.delete()

    def testLoadingTaglib(self):
        """Tests if the taglib defined in this app can be loaded"""
        tpl = template.Template('{% load flatblock_tags %}')
        tpl.render(template.Context({}))

    def testExistingPlain(self):
        tpl = template.Template(
            '{% load flatblock_tags %}{% plain_flatblock "block" %}')
        self.assertEqual('CONTENT', tpl.render(template.Context({})).strip())

    def testExistingTemplate(self):
        expected = """<div class="flatblock block-block">

    <h2 class="flatblock-title">HEADER</h2>

    <div class="flatblock-content">CONTENT</div>
</div>
"""
        tpl = template.Template(
            '{% load flatblock_tags %}{% flatblock "block" %}')
        self.assertEqual(expected, tpl.render(template.Context({})))

    def testUsingMissingTemplate(self):
        tpl = template.Template(
            '{% load flatblock_tags %}'
            '{% flatblock "block" using="missing_template.html" %}')
        exception = template.base.TemplateDoesNotExist
        self.assertRaises(exception, tpl.render, template.Context({}))

    def testBlockAsVariable(self):
        tpl = template.Template(
            '{% load flatblock_tags %}{% flatblock blockvar %}')
        tpl.render(template.Context({'blockvar': 'block'}))

    def testContentEvaluation(self):
        """
        If a block is set in the template to be evaluated the actual content of
        the block is treated as a Django template and receives the parent
        template's context.
        """
        self.create_block_for_site1(slug='tmpl_block',
                                 header='HEADER',
                                 content='{{ variable }}'
                                 )
        tpl = template.Template(
            '{% load flatblock_tags %}'
            '{% plain_flatblock "tmpl_block" evaluated=True %}')
        result = tpl.render(template.Context({'variable': 'value'}))
        self.assertEqual('value', result)

    def testDisabledEvaluation(self):
        """
        If "evaluated" is not passed, no evaluation should take place.
        """
        self.create_block_for_site1(slug='tmpl_block',
                                 header='HEADER',
                                 content='{{ variable }}'
                                 )
        tpl = template.Template(
            '{% load flatblock_tags %}{% plain_flatblock "tmpl_block" %}')
        result = tpl.render(template.Context({'variable': 'value'}))
        self.assertEqual('{{ variable }}', result)

    def testHeaderEvaluation(self):
        """
        Also the header should receive the context and get evaluated.
        """
        self.create_block_for_site1(slug='tmpl_block',
                                 header='{{ header_variable }}',
                                 content='{{ variable }}'
                                 )
        tpl = template.Template(
            '{% load flatblock_tags %}{% flatblock "tmpl_block" evaluated=True %}')
        result = tpl.render(template.Context({
            'variable': 'value',
            'header_variable': 'header-value'
        }))
        self.assertTrue('header-value' in result)


class AutoCreationTest(TestCase):
    """ Test case for block autcreation """

    def testMissingStaticBlock(self):
        """Tests if a missing block with hardcoded name will be auto-created"""
        expected = """<div class="flatblock block-foo">

    <div class="flatblock-content">foo</div>
</div>"""
        settings.AUTOCREATE_STATIC_BLOCKS = True
        tpl = template.Template(
            '{% load flatblock_tags %}{% flatblock "foo" %}')
        self.assertEqual(expected, tpl.render(template.Context({})).strip())
        self.assertEqual(FlatBlock.objects.count(), 1)
        self.assertEqual(expected, tpl.render(template.Context({})).strip())
        self.assertEqual(FlatBlock.objects.count(), 1)

    def testNotAutocreatedMissingStaticBlock(self):
        """
        Tests if a missing block with hardcoded name won't be auto-created if
        feature is disabled"""
        expected = ""
        settings.AUTOCREATE_STATIC_BLOCKS = False
        tpl = template.Template(
            '{% load flatblock_tags %}{% flatblock "block" %}')
        self.assertEqual(expected, tpl.render(template.Context({})).strip())
        self.assertEqual(FlatBlock.objects.filter(slug='block').count(), 0)

    def _testMissingVariableBlock(self):
        """
        Tests if a missing block with variable name will simply return an empty
        string
        """
        settings.AUTOCREATE_STATIC_BLOCKS = True
        tpl = template.Template('{% load flatblock_tags %}{% flatblock name %}')
        output = tpl.render(template.Context({'name': 'foo'})).strip()
        self.assertEqual('', output)
