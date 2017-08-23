# -*- coding:utf8 -*-

from __future__ import unicode_literals

from factory import Sequence

from wagtail_factories import PageFactory

from wagtail_library.models import LibraryIndex, LibraryDetail


class LibraryIndexFactory(PageFactory):
    title = Sequence('Library index {}'.format)
    body = Sequence('Library index {} body.'.format)

    class Meta(object):
        """Factory properties."""
        model = LibraryIndex


class LibraryDetailFactory(PageFactory):
    title = Sequence('Library detail {}'.format)
    body = Sequence('Library detail {} body.'.format)

    class Meta(object):
        """Factory properties."""
        model = LibraryDetail
