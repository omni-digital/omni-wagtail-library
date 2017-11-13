# -*- coding: utf-8 -*-
"""Tests for wagtail_library models."""

from __future__ import unicode_literals

import os

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.paginator import Paginator, Page as PaginatorPage
from django.db import models
from django.test import RequestFactory, TestCase, override_settings
from mock import Mock, patch
from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField

from wagtail_library import abstract_models
from wagtail_library.models import LibraryIndex, LibraryDetail

from tests.factories import LibraryIndexFactory, LibraryDetailFactory


BASE_DIR = os.path.join(settings.PROJECT_DIR, 'tests/assets')


@override_settings(MEDIA_ROOT=BASE_DIR)
class TestLibraryIndex(TestCase):
    """Tests for the LibraryIndex model."""
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
        self.index = LibraryIndexFactory.create(
            paginate_by=10,
            parent=None,
        )
        self.detail_one = LibraryDetailFactory.create(
            attachment=self.get_file(),
            parent=self.index,
        )
        self.detail_two = LibraryDetailFactory.create(
            attachment=self.get_file(),
            live=False,
            parent=self.index,
        )
        self.model = LibraryIndex
        self.request = RequestFactory().get('')
        self.request.is_preview = False

    def test_inheritance(self):
        """LibraryIndex should subclass AbstractLibraryIndex."""
        self.assertTrue(issubclass(self.model, Page))
        self.assertTrue(issubclass(
            self.model,
            abstract_models.AbstractLibraryIndex
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
        """LibraryIndex.get_context should create valid template context."""
        context = self.index.get_context(self.request)

        self.assertIn('queryset', context)
        self.assertIn('children', context)
        self.assertTrue(context.get('is_paginated'))

    def test_get_paginator_class(self):
        """The default implementation of _get_paginator_class should return djangos paginator"""
        # Test the default implementation returns the expected class
        self.assertEqual(self.index.get_paginator_class(), Paginator)

        # Test the overridden implementation returns the expected class
        self.index.paginator_class = Mock()
        self.assertEqual(
            self.index.get_paginator_class(),
            self.index.paginator_class
        )

    def test_get_paginator(self):
        """The _get_paginator method should return a paginator instance"""
        object_list = ['foo', 'bar', 'baz']
        paginator = self.index.get_paginator(object_list, 1)
        self.assertIsInstance(paginator, Paginator)
        self.assertEqual(paginator.object_list, object_list)
        self.assertEqual(3, paginator.num_pages)

    def test_paginate_queryset(self):
        """paginate_queryset should return page and paginator."""
        self.request.is_preview = True
        children = self.index._get_children(self.request)
        page, paginator = self.index.paginate_queryset(children, 1)

        self.assertIsInstance(page, PaginatorPage)
        self.assertIsInstance(paginator, Paginator)
        self.assertEqual(paginator.per_page, self.index.paginate_by)
        self.assertEqual(paginator.num_pages, 1)

    @patch(
        'wagtail_library.abstract_models.AbstractLibraryIndex.get_paginator_kwargs',
        Mock(return_value={'foo': 'bar'})
    )
    @patch('wagtail_library.abstract_models.AbstractLibraryIndex.get_paginator')
    def test_paginate_queryset_calls_get_paginator(self, get_paginator):
        """paginate_queryset should call the get_paginator method."""
        self.request.is_preview = True
        children = self.index._get_children(self.request)
        self.index.paginate_queryset(children, 1)
        get_paginator.assert_called_with(children, self.index.paginate_by, foo='bar')

    def test_paginate_without_qs(self):
        """If now querystrings are provided return the first page."""
        queryset = self.index._get_children(self.request)
        response = self.index.paginate_queryset(queryset, '')

        self.assertEqual(response[0].number, 1)

    def test_paginate_qs_non_int(self):
        """If page number is not an integer return the first page."""
        queryset = self.index._get_children(self.request)
        response = self.index.paginate_queryset(queryset, 'foo')

        self.assertEqual(response[0].number, 1)

    def test_paginate_qs_page_empty_page(self):
        """If page number is too large - return the last page."""
        queryset = self.index._get_children(self.request)
        response = self.index.paginate_queryset(queryset, 2)

        self.assertEqual(response[0].paginator.num_pages, response[0].number)

    @patch('wagtail_library.abstract_models.AbstractLibraryIndex.get_additional_filter_kwargs')
    def test_get_children_additional_filters(self, patched_filter):
        """_get_children should respect additional filters."""
        self.request.is_preview = False
        patched_filter.return_value = {
            'title': self.detail_one.title,
        }
        children = self.index._get_children(self.request)
        self.assertEqual(len(children), 1)
        self.assertEqual(children[0], self.detail_one)


class TestLibraryDetail(TestCase):
    """Test for the LibraryDetail."""
    def setUp(self):
        super(TestLibraryDetail, self).setUp()
        self.model = LibraryDetail

    def test_inheritance(self):
        """LibraryDetail should subclass AbstractLibraryDetail."""
        self.assertTrue(issubclass(self.model, Page))
        self.assertTrue(issubclass(
            self.model,
            abstract_models.AbstractLibraryDetail
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
