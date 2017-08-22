# -*- coding:utf8 -*-
"""
Application models
"""

from __future__ import unicode_literals

from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailcore.fields import RichTextField

from wagtail_library import abstract_models as abstracts


class LibraryIndexPage(abstracts.AbstractLibraryIndexPage):
    """Library index page."""
    body = RichTextField()

    content_panels = abstracts.AbstractLibraryIndexPage.content_panels + [
        FieldPanel('body'),
    ]
    subpage_types = ['wagtail_library.LibraryItemDetailPage']


class LibraryItemDetailPage(abstracts.AbstractLibraryItemDetailPage):
    """Library item detail page."""
    body = RichTextField()

    parent_page_types = ['wagtail_library.LibraryIndexPage']
    content_panels = abstracts.AbstractLibraryItemDetailPage.content_panels + [
        FieldPanel('body'),
    ]
