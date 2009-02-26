import unittest

from django import template

from flatblocks import models


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
        # Actually we should be listening to a TemplateDoesNotExist exception
        # but Django masks those.
        exception = template.TemplateSyntaxError
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

