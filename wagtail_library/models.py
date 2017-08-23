# -*- coding:utf8 -*-
"""wagtail_library models"""

from __future__ import unicode_literals

from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailcore.fields import RichTextField

from wagtail_library import abstract_models


class LibraryIndex(abstract_models.AbstractLibraryIndex):
    """Library index page."""
    body = RichTextField()

    content_panels = abstract_models.AbstractLibraryIndex.content_panels + [
        FieldPanel('body'),
    ]
    subpage_types = ['wagtail_library.LibraryDetail']


class LibraryDetail(abstract_models.AbstractLibraryDetail):
    """Library item detail page."""
    body = RichTextField()

    content_panels = abstract_models.AbstractLibraryDetail.content_panels + [
        FieldPanel('body'),
    ]
    parent_page_types = ['wagtail_library.LibraryIndex']
    subpage_types = []
