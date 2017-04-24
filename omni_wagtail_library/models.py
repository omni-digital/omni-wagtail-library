# -*- coding:utf8 -*-
"""
Application models
"""

from __future__ import unicode_literals

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import models

from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.wagtailcore.blocks import PageChooserBlock
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailcore.models import Page


class AbstractLibraryListingPage(Page):
    """
    Abstract library listing page
    """
    paginate_by = models.PositiveIntegerField(
        blank=True,
        null=True
    )

    content_panels = Page.content_panels + [
        FieldPanel('paginate_by'),
    ]

    class Meta(object):
        """
        Django model meta options
        """
        abstract = True

    def _get_children(self, request):
        """
        Helper method for getting child nodes to display in the listing
        :param request: django request
        :return: Queryset of child model instances
        """
        model_class = self.__class__.allowed_subpage_models()[0]
        children = model_class.objects.child_of(self)
        if not request.is_preview:
            children = children.filter(live=True)
        return children

    def _paginate_queryset(self, queryset, page):
        """
        Helper method for paginating the queryset provided
        :param queryset: Queryset of model instances to paginate
        :param page: Raw page number taken from the request dict
        :return: Queryset of child model instances
        """
        paginator = Paginator(queryset, self.paginate_by)
        try:
            queryset = paginator.page(page)
        except PageNotAnInteger:
            queryset = paginator.page(1)
        except EmptyPage:
            queryset = paginator.page(paginator.num_pages)
        return queryset, paginator

    def get_context(self, request, *args, **kwargs):
        """
        Adds child pages to the context and paginates them if pagination is required
        :param request: HttpRequest instance
        :param args: default positional args
        :param kwargs: default keyword args
        :return: Context data to use when rendering the template
        """
        context = super(AbstractLibraryListingPage, self).get_context(request, *args, **kwargs)
        queryset = children = self._get_children(request)
        is_paginated = False
        paginator = None

        # Paginate the child nodes if paginate_by has been specified
        if self.paginate_by:
            is_paginated = True
            children, paginator = self._paginate_queryset(children, request.GET.get('page'))

        context.update(
            queryset=queryset,
            children=children,
            paginator=paginator,
            is_paginated=is_paginated
        )
        return context


class LibraryListingPage(AbstractLibraryListingPage):
    """
    Common features
    """
    content = RichTextField()

    content_panels = Page.content_panels + [
        FieldPanel('content'),
        FieldPanel('paginate_by'),
    ]


class AbstractLibraryItemDetailPage(Page):
    """
    Abstract library item detail page
    """

    attachment = models.FileField(upload_to='attachments')
    content_panels = Page.content_panels + [
        FieldPanel('attachment'),
    ]

    class Meta(object):
        """
        Django properties
        """
        abstract = True


class LibraryItemBlock(PageChooserBlock):

    def __init__(self, **kwargs):
        self._target_model = 'omni_wagtail_library.LibraryItemDetailPage'
        self._template = 'omni_wagtail_library/library_item_block.html'
        super(LibraryItemBlock, self).__init__(**kwargs)


class LibraryItemDetailPage(AbstractLibraryItemDetailPage):
    """
    Library item detail page
    """
    content = StreamField([('content', LibraryItemBlock())], blank=True, null=True)
    parent_page_types = ['LibraryListingPage']
    content_panels = Page.content_panels + [
        StreamFieldPanel('content'),
        FieldPanel('attachment'),
    ]
