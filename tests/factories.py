# -*- coding:utf8 -*-

from __future__ import unicode_literals

from factory import Sequence

from wagtail_factories import PageFactory

from wagtail_library.models import LibraryIndexPage, LibraryItemDetailPage


class LibraryIndexPageFactory(PageFactory):
    title = Sequence('Library index {}'.format)
    body = Sequence('Library index {} body.'.format)

    class Meta(object):
        """Factory properties."""
        model = LibraryIndexPage


class LibraryItemDetailPageFactory(PageFactory):
    title = Sequence('Library item detail {}'.format)
    body = Sequence('Library item detail {} body.'.format)

    class Meta(object):
        """Factory properties."""
        model = LibraryItemDetailPage
