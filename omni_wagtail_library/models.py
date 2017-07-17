# -*- coding:utf8 -*-
"""
Application models
"""

from __future__ import unicode_literals

from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.wagtailcore.blocks import RichTextBlock
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailcore.models import Page
from wagtail.wagtailimages.blocks import ImageChooserBlock

from omni_wagtail_library import abstract_models


class LibraryListingPage(abstract_models.AbstractLibraryListingPage):
    """
    Common features
    """
    content = RichTextField()

    content_panels = Page.content_panels + [
        FieldPanel('content'),
        FieldPanel('paginate_by'),
    ]
    subpage_types = ['omni_wagtail_library.LibraryItemDetailPage']


class LibraryItemDetailPage(abstract_models.AbstractLibraryItemDetailPage):
    """
    Library item detail page
    """
    content = StreamField([
        ('paragraph', RichTextBlock()),
        ('image', ImageChooserBlock())
    ], blank=True, null=True)
    parent_page_types = ['LibraryListingPage']
    content_panels = Page.content_panels + [
        StreamFieldPanel('content'),
        FieldPanel('attachment'),
    ]
