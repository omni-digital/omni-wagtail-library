# -*- coding: utf-8 -*-
"""
Tests the application models
"""
from __future__ import unicode_literals

import os

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import models
from django.template.defaultfilters import slugify
from django.test import RequestFactory, TestCase, override_settings
from django.utils.crypto import get_random_string
from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField

from omni_wagtail_library import abstract_models
from omni_wagtail_library.models import LibraryListingPage, LibraryItemDetailPage


BASE_DIR = os.path.join(settings.PROJECT_DIR, 'omni_wagtail_library/tests/assets')
FAKE_PATH = '/{0}/'.format(get_random_string())


@override_settings(MEDIA_ROOT=BASE_DIR)
class TestCaseStub(TestCase):
    """
    Testing stub for temporal content
    """

    listing_model = LibraryListingPage
    item_model = LibraryItemDetailPage

    @staticmethod
    def get_file():
        """
        Dummy file handler

        :return: File instance ready to be used in django models
        """
        return SimpleUploadedFile(
            name='image.jpg',
            content=open(os.path.join(BASE_DIR, 'image.jpg'), 'rb').read(),
            content_type='image/jpeg')

    def create_detail_factory(self, **kwargs):
        """
        Create factory of the `self.item_model` from the default parameters
        :param kwargs:
        :return: Created factory
        """
        def get_value(key, default):
            val = kwargs.get(key)
            return default if val is None else val

        title = get_value('title', get_random_string())
        params = {
            'title': title,
            'slug': get_value('slug', slugify(title)),
            'content': get_value('content', '<p>{0}</p>'.format(get_random_string())),
            'attachment': get_value('attachment', self.get_file()),
            'live': get_value('live', True)
        }
        return self.item_model(**params)

    def setUp(self):
        """
        Setting up the test case
        """
        super(TestCaseStub, self).setUp()

        home_page_title = get_random_string()
        self.home_page = Page.add_root(title=home_page_title, live=True, slug=slugify(home_page_title))

        self.listing_page = self.home_page.add_child(
            instance=self.listing_model(
                title='listing',
                slug='listing',
                content='<p>This is the listing page</p>',
                paginate_by=2,
                live=True
            )
        )
        self.detail_page_1 = self.listing_page.add_child(instance=self.create_detail_factory())
        self.detail_page_2 = self.listing_page.add_child(instance=self.create_detail_factory(live=False))
        self.detail_page_3 = self.listing_page.add_child(instance=self.create_detail_factory())
        self.detail_page_4 = self.listing_page.add_child(instance=self.create_detail_factory())
        self.detail_page_5 = self.listing_page.add_child(instance=self.create_detail_factory(live=False))
        self.detail_page_6 = self.listing_page.add_child(instance=self.create_detail_factory())


class LibraryListingPageSimpleTestCase(TestCaseStub):
    """
    Tests the LibraryListingPage
    """

    model = LibraryListingPage

    def setUp(self):
        """
        Setting up the test case
        """
        super(LibraryListingPageSimpleTestCase, self).setUp()
        self.preview_request = self.get_request(preview=True)
        self.production_request = self.get_request(preview=False)

    def test_inheritance(self):
        """LibraryListingPage should subclass AbstractLibraryListingPage."""
        self.assertTrue(issubclass(self.model, Page))
        self.assertTrue(issubclass(
            self.model,
            abstract_models.AbstractLibraryListingPage
        ))

    def get_request(self, preview):
        request = RequestFactory().get(FAKE_PATH)
        request.is_preview = preview
        return request

    def test_paginate_by_field(self):
        """ The model should have a paginate_by field """
        field = self.model._meta.get_field('paginate_by')
        self.assertIsInstance(field, models.PositiveIntegerField)
        self.assertTrue(field.blank)
        self.assertTrue(field.null)

    def test_content_panels(self):
        """ The models content_panels should include the content and paginate_by fields """
        self.assertIn('paginate_by', [panel.field_name for panel in self.model.content_panels])

    def test_get_children_preview_mode(self):
        """ Should have all nodes in child list """
        ids = self.listing_page._get_children(self.preview_request).values_list('id', flat=True)
        self.assertIn(self.detail_page_1.pk, ids)
        self.assertIn(self.detail_page_2.pk, ids)

    def test_get_children_production_mode(self):
        """ Should have only published nodes in child list """
        ids = self.listing_page._get_children(self.production_request).values_list('id', flat=True)
        self.assertIn(self.detail_page_1.pk, ids)
        self.assertNotIn(self.detail_page_2.pk, ids)

    def test_context(self):
        """ Should generate valid template context """
        context = self.listing_page.get_context(self.production_request)
        self.assertIn('queryset', context)
        self.assertIn('children', context)
        self.assertTrue(context.get('is_paginated'))

    def test_paginate_qs_page(self):
        """ If page number is not an integer - return the first page """
        queryset = self.listing_page._get_children(self.production_request)
        response = self.listing_page._paginate_queryset(queryset, get_random_string())
        self.assertEqual(len(response[0]), self.listing_page.paginate_by)
        self.assertEqual(response[0].number, 1)

    def test_paginate_qs_page_nan(self):
        """ If page number is not an integer - return the first page """
        queryset = self.listing_page._get_children(self.production_request)
        response = self.listing_page._paginate_queryset(queryset, get_random_string())
        self.assertEqual(len(response[0]), self.listing_page.paginate_by)
        self.assertEqual(response[0].number, 1)

    def test_paginate_qs_page_empty_page(self):
        """ If page number is too large - return the last page """
        queryset = self.listing_page._get_children(self.production_request)
        response = self.listing_page._paginate_queryset(queryset, 666)
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

    def test_content_field(self):
        """The content field should be an instance of StreamField."""
        field = self.model._meta.get_field('content')

        self.assertIsInstance(field, StreamField)
