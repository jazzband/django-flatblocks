from django import template
from django.test import TestCase
from django.contrib.auth.models import User
from django import db

from flatblocks.models import FlatBlock
from flatblocks import settings


class BasicTests(TestCase):

    def setUp(self):
        self.testblock = FlatBlock.objects.create(slug='block',
                                                  header='HEADER',
                                                  content='CONTENT'
                                                  )
        self.admin = User.objects.create_superuser('admin', 'admin@localhost',
                                                   'adminpwd')

    def testURLConf(self):
        resp = self.client.get('/flatblocks/edit/1/', follow=True)
        self.assertTemplateUsed(resp, 'admin/login.html')
        self.client.login(username='admin', password='adminpwd')
        resp = self.client.get('/flatblocks/edit/1/')
        self.assertTemplateUsed(resp, 'flatblocks/edit.html')

    def testSaveForceUpdate(self):
        block = FlatBlock(slug='missing')
        with self.assertRaises(ValueError):
            block.save(force_update=True)

    def testSaveForceInsert(self):
        block = FlatBlock.objects.get(slug='block')
        with self.assertRaises(db.IntegrityError):
            block.save(force_insert=True)


class TagTests(TestCase):
    def setUp(self):
        self.testblock = FlatBlock.objects.create(slug='block',
                                                  header='HEADER',
                                                  content='CONTENT'
                                                  )

    def testLoadingTaglib(self):
        """Tests if the taglib defined in this app can be loaded"""
        tpl = template.Template('{% load flatblocks %}')
        tpl.render(template.Context({}))

    def testExistingPlain(self):
        tpl = template.Template('{% load flatblocks %}{% plain_flatblock "block" %}')
        self.assertEqual('CONTENT', tpl.render(template.Context({})).strip())

    def testExistingTemplate(self):
        expected = """<div class="flatblock block-block">

    <h2 class="flatblock-title">HEADER</h2>

    <div class="flatblock-content">CONTENT</div>
</div>
"""
        tpl = template.Template('{% load flatblocks %}{% flatblock "block" %}')
        self.assertEqual(expected, tpl.render(template.Context({})))

    def testUsingMissingTemplate(self):
        tpl = template.Template(
            '{% load flatblocks %}'
            '{% flatblock "block" using="missing_template.html" %}')
        exception = template.base.TemplateDoesNotExist
        self.assertRaises(exception, tpl.render, template.Context({}))

    def testBlockAsVariable(self):
        tpl = template.Template(
            '{% load flatblocks %}{% flatblock blockvar %}')
        tpl.render(template.Context({'blockvar': 'block'}))

    def testContentEvaluation(self):
        """
        If a block is set in the template to be evaluated the actual content of
        the block is treated as a Django template and receives the parent
        template's context.
        """
        FlatBlock.objects.create(slug='tmpl_block',
                                 header='HEADER',
                                 content='{{ variable }}'
                                 )
        tpl = template.Template(
            '{% load flatblocks %}'
            '{% plain_flatblock "tmpl_block" evaluated=True %}')
        result = tpl.render(template.Context({'variable': 'value'}))
        self.assertEqual('value', result)

    def testDisabledEvaluation(self):
        """
        If "evaluated" is not passed, no evaluation should take place.
        """
        FlatBlock.objects.create(slug='tmpl_block',
                                 header='HEADER',
                                 content='{{ variable }}'
                                 )
        tpl = template.Template(
            '{% load flatblocks %}{% plain_flatblock "tmpl_block" %}')
        result = tpl.render(template.Context({'variable': 'value'}))
        self.assertEqual('{{ variable }}', result)

    def testHeaderEvaluation(self):
        """
        Also the header should receive the context and get evaluated.
        """
        FlatBlock.objects.create(slug='tmpl_block',
                                 header='{{ header_variable }}',
                                 content='{{ variable }}'
                                 )
        tpl = template.Template(
            '{% load flatblocks %}{% flatblock "tmpl_block" evaluated=True %}')
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
        tpl = template.Template('{% load flatblocks %}{% flatblock "foo" %}')
        settings.AUTOCREATE_STATIC_BLOCKS = True
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
            '{% load flatblocks %}{% flatblock "block" %}')
        self.assertEqual(expected, tpl.render(template.Context({})).strip())
        self.assertEqual(FlatBlock.objects.filter(slug='block').count(), 0)

    def _testMissingVariableBlock(self):
        """
        Tests if a missing block with variable name will simply return an empty
        string
        """
        settings.AUTOCREATE_STATIC_BLOCKS = True
        tpl = template.Template('{% load flatblocks %}{% flatblock name %}')
        output = tpl.render(template.Context({'name': 'foo'})).strip()
        self.assertEqual('', output)
