# -*- coding: utf-8 -*-
"""Tests omni_wagtail_library blocks."""
from __future__ import unicode_literals

from django.test import TestCase
from wagtail.wagtailcore.blocks import PageChooserBlock

from omni_wagtail_library.blocks import LibraryItemBlock


class LibraryItemBlockTestCase(TestCase):
    """
    Testing stub for temporal content
    """
    def test_inheritance(self):
        """
        The block should subclass PageChooserBlock
        """
        self.assertTrue(issubclass(LibraryItemBlock, PageChooserBlock))

    def test_template(self):
        """
        The block should use the correct template
        """
        self.assertEqual(LibraryItemBlock._meta_class.template, 'omni_wagtail_library/library_item_block.html')
