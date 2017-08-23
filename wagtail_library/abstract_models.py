# -*- coding:utf8 -*-
"""Abstract models"""

from __future__ import unicode_literals

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import models
from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailcore.models import Page


class AbstractLibraryIndex(Page):
    """Abstract library index page."""
    paginate_by = models.PositiveIntegerField(
        blank=True,
        null=True
    )

    content_panels = Page.content_panels + [FieldPanel('paginate_by')]

    class Meta(object):
        """Django model meta options."""
        abstract = True

    def _get_children(self, request):
        """
        Helper method for getting child nodes to display in the index.

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
        Helper method for paginating the queryset provided.

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
        Adds child pages to the context and paginates if required.

        :param request: HttpRequest instance
        :param args: default positional args
        :param kwargs: default keyword args
        :return: Context data to use when rendering the template
        """
        context = super(AbstractLibraryIndex, self).get_context(
            request,
            *args,
            **kwargs
        )
        queryset = children = self._get_children(request)
        is_paginated = False
        paginator = None

        # Paginate the child nodes if paginate_by has been specified
        if self.paginate_by:
            is_paginated = True
            children, paginator = self._paginate_queryset(
                children,
                request.GET.get('page'),
            )

        context.update(
            queryset=queryset,
            children=children,
            paginator=paginator,
            is_paginated=is_paginated
        )
        return context


class AbstractLibraryDetail(Page):
    """Abstract library item detail page."""

    attachment = models.FileField(upload_to='attachments')
    content_panels = Page.content_panels + [FieldPanel('attachment')]

    class Meta(object):
        """Django properties."""
        abstract = True
