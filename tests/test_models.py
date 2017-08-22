# -*- coding: utf-8 -*-
"""Tests for wagtail_library models."""

from __future__ import unicode_literals

import os

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import models
from django.test import RequestFactory, TestCase, override_settings
from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField

from wagtail_library import abstract_models
from wagtail_library.models import LibraryIndexPage, LibraryItemDetailPage

from tests.factories import LibraryIndexPageFactory, LibraryItemDetailPageFactory


BASE_DIR = os.path.join(settings.PROJECT_DIR, 'tests/assets')


@override_settings(MEDIA_ROOT=BASE_DIR)
class TestLibraryIndexPage(TestCase):
    """Tests for the LibraryIndexPage model."""
    @staticmethod
    def get_file():
        """
        Dummy file handler

        :return: File instance ready to be used in django models
        """
        return SimpleUploadedFile(
            name='image.jpg',
            content=open(os.path.join(BASE_DIR, 'image.jpg'), 'rb').read(),
            content_type='image/jpeg',
        )

    def setUp(self):
        self.index = LibraryIndexPageFactory.create(
            paginate_by=10,
            parent=None,
        )
        self.detail_one = LibraryItemDetailPageFactory.create(
            attachment=self.get_file(),
            parent=self.index,
        )
        self.detail_two = LibraryItemDetailPageFactory.create(
            attachment=self.get_file(),
            live=False,
            parent=self.index,
        )
        self.model = LibraryIndexPage
        self.request = RequestFactory().get('')
        self.request.is_preview = False

    def test_inheritance(self):
        """LibraryIndexPage should subclass AbstractLibraryIndexPage."""
        self.assertTrue(issubclass(self.model, Page))
        self.assertTrue(issubclass(
            self.model,
            abstract_models.AbstractLibraryIndexPage
        ))

    def test_paginate_by_field(self):
        """The model should have a paginate_by field."""
        field = self.model._meta.get_field('paginate_by')

        self.assertIsInstance(field, models.PositiveIntegerField)
        self.assertTrue(field.blank)
        self.assertTrue(field.null)

    def test_body_field(self):
        """The body field should be an instance of RichTextField."""
        field = self.model._meta.get_field('body')

        self.assertIsInstance(field, RichTextField)

    def test_content_panels(self):
        """The content_panels should include the paginate_by & body fields."""
        self.assertIn(
            'paginate_by',
            [panel.field_name for panel in self.model.content_panels],
        )
        self.assertIn(
            'body',
            [panel.field_name for panel in self.model.content_panels],
        )

    def test_get_children_preview_mode(self):
        """Should have all nodes in child list."""
        self.request.is_preview = True
        ids = self.index._get_children(self.request).values_list(
            'id',
            flat=True,
        )

        self.assertIn(self.detail_one.pk, ids)
        self.assertIn(self.detail_two.pk, ids)

    def test_get_children_production_mode(self):
        """Should have only published nodes in child list."""
        ids = self.index._get_children(self.request).values_list(
            'id',
            flat=True,
        )

        self.assertIn(self.detail_one.pk, ids)
        self.assertNotIn(self.detail_two.pk, ids)

    def test_get_context(self):
        """LibraryIndexPage.get_context should create valid template context."""
        context = self.index.get_context(self.request)

        self.assertIn('queryset', context)
        self.assertIn('children', context)
        self.assertTrue(context.get('is_paginated'))

    def test_paginate_without_qs(self):
        """If now querystrings are provided return the first page."""
        queryset = self.index._get_children(self.request)
        response = self.index._paginate_queryset(queryset, '')

        self.assertEqual(response[0].number, 1)

    def test_paginate_qs_non_int(self):
        """If page number is not an integer return the first page."""
        queryset = self.index._get_children(self.request)
        response = self.index._paginate_queryset(queryset, 'foo')

        self.assertEqual(response[0].number, 1)

    def test_paginate_qs_page_empty_page(self):
        """If page number is too large - return the last page."""
        queryset = self.index._get_children(self.request)
        response = self.index._paginate_queryset(queryset, 2)

        self.assertEqual(response[0].paginator.num_pages, response[0].number)


class TestLibraryItemDetailPage(TestCase):
    """Test for the LibraryItemDetailPage."""
    def setUp(self):
        super(TestLibraryItemDetailPage, self).setUp()
        self.model = LibraryItemDetailPage

    def test_inheritance(self):
        """LibraryItemDetailPage should subclass AbstractLibraryItemDetailPage."""
        self.assertTrue(issubclass(self.model, Page))
        self.assertTrue(issubclass(
            self.model,
            abstract_models.AbstractLibraryItemDetailPage
        ))

    def test_body_field(self):
        """The body field should be an instance of RichTextField."""
        field = self.model._meta.get_field('body')

        self.assertIsInstance(field, RichTextField)

    def test_content_panels(self):
        """The content_panels should include the body & attachment fields."""
        self.assertIn(
            'attachment',
            [panel.field_name for panel in self.model.content_panels],
        )
        self.assertIn(
            'body',
            [panel.field_name for panel in self.model.content_panels],
        )
