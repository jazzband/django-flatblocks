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
            if isinstance(resp.template, list):
                return resp.template[0]
            return resp.template
        self.assertEquals(get_tmpl(self.client.get('/edit/1/')).name, 'admin/login.html')
        self.client.login(username='admin', password='adminpwd')
        self.assertEquals(get_tmpl(self.client.get('/edit/1/')).name, 'flatblocks/edit.html')

    def testCacheReset(self):
        """
        Tests if FlatBlock.save() resets the cache.
        """
        tpl = template.Template('{% load flatblock_tags %}{% flatblock "block" 60 %}')
        tpl.render(template.Context({}))
        name = '%sblock' % settings.CACHE_PREFIX
        self.assertNotEquals(None, cache.get(name))
        block = FlatBlock.objects.get(slug='block')
        block.header = 'UPDATED'
        block.save()
        self.assertEquals(None, cache.get(name))

    def testSaveKwargs(self):
        block = FlatBlock(slug='missing')
#        block.slug = 'missing'
        self.assertRaises(ValueError, block.save, force_update=True)
        block = FlatBlock.objects.get(slug='block')
        self.assertRaises(db.IntegrityError, block.save, force_insert=True)

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
        tpl = template.Template('{% load flatblock_tags %}{% plain_flatblock "block" %}')
        self.assertEqual(u'CONTENT', tpl.render(template.Context({})).strip())

    def testExistingTemplate(self):
        expected = """<div class="flatblock block-block">

    <h2 class="title">HEADER</h2>

    <div class="content">CONTENT</div>
</div>
"""
        tpl = template.Template('{% load flatblock_tags %}{% flatblock "block" %}')
        self.assertEqual(expected, tpl.render(template.Context({})))

    def testUsingMissingTemplate(self):
        tpl = template.Template('{% load flatblock_tags %}{% flatblock "block" using "missing_template.html" %}')
        exception = template.TemplateSyntaxError
        self.assertRaises(exception, tpl.render, template.Context({}))

    def testSyntax(self):
        tpl = template.Template('{% load flatblock_tags %}{% flatblock "block" %}')
        tpl.render(template.Context({}))
        tpl = template.Template('{% load flatblock_tags %}{% flatblock "block" 123 %}')
        tpl.render(template.Context({}))
        tpl = template.Template('{% load flatblock_tags %}{% flatblock "block" using "flatblocks/flatblock.html" %}')
        tpl.render(template.Context({}))
        tpl = template.Template('{% load flatblock_tags %}{% flatblock "block" 123 using "flatblocks/flatblock.html" %}')
        tpl.render(template.Context({}))

    def testBlockAsVariable(self):
        tpl = template.Template('{% load flatblock_tags %}{% flatblock blockvar %}')
        tpl.render(template.Context({'blockvar': 'block'}))


class AutoCreationTest(TestCase):
    """ Test case for block autcreation """

    def testMissingStaticBlock(self):
        """Tests if a missing block with hardcoded name will be auto-created"""
        expected = """<div class="flatblock block-foo">

    <div class="content">foo</div>
</div>"""
        settings.AUTOCREATE_STATIC_BLOCKS = True
        tpl = template.Template('{% load flatblock_tags %}{% flatblock "foo" %}')
        self.assertEqual(expected, tpl.render(template.Context({})).strip())
        self.assertEqual(FlatBlock.objects.count(), 1)
        self.assertEqual(expected, tpl.render(template.Context({})).strip())
        self.assertEqual(FlatBlock.objects.count(), 1)

    def testNotAutocreatedMissingStaticBlock(self):
        """Tests if a missing block with hardcoded name won't be auto-created if feature is disabled"""
        expected = u""
        settings.AUTOCREATE_STATIC_BLOCKS = False
        tpl = template.Template('{% load flatblock_tags %}{% flatblock "block" %}')
        self.assertEqual(expected, tpl.render(template.Context({})).strip())
        self.assertEqual(FlatBlock.objects.filter(slug='block').count(), 0)

    def testMissingVariableBlock(self):
        settings.AUTOCREATE_STATIC_BLOCKS = True
        """Tests if a missing block with variable name will simply return an empty string"""
        tpl = template.Template('{% load flatblock_tags %}{% flatblock name %}')
        self.assertEqual('', tpl.render(template.Context({'name': 'foo'})).strip())


