# -*- coding: utf-8 -*-
"""Tests for wagtail_library blocks."""

from __future__ import unicode_literals

from django.test import TestCase
from wagtail.wagtailcore.blocks import PageChooserBlock

from wagtail_library.blocks import LibraryItemBlock
from wagtail_library.models import LibraryItemDetailPage


class TestLibraryItemblock(TestCase):
    """Test for the LibraryItemBlock."""
    def test_inheritance(self):
        """The block should subclass PageChooserBlock."""
        self.assertTrue(issubclass(LibraryItemBlock, PageChooserBlock))

    def test_template(self):
        """The block should use the correct template."""
        self.assertEqual(
            LibraryItemBlock._meta_class.template,
            'wagtail_library/library_item_block.html')

    def test_target_model(self):
        """The block should have the correct target_model."""
        block = LibraryItemBlock()

        self.assertEqual(block.target_model, LibraryItemDetailPage)
