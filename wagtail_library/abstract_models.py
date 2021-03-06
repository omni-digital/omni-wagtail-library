# -*- coding:utf8 -*-
"""Abstract models"""

from __future__ import unicode_literals

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import models
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.models import Page


class AbstractLibraryIndex(Page):
    """Abstract library index page."""

    paginate_by = models.PositiveIntegerField(blank=True, null=True)

    content_panels = Page.content_panels + [FieldPanel("paginate_by")]
    paginator_class = Paginator

    class Meta(object):
        """Django model meta options."""

        abstract = True

    def _get_children(self, request, *args, **kwargs):
        """
        Helper method for getting child nodes to display in the index.

        :param request: django request
        :return: Queryset of child model instances
        """
        model_class = self.__class__.allowed_subpage_models()[0]
        children = model_class.objects.child_of(self)
        if not request.is_preview:
            children = children.filter(live=True)
        return children.filter(**self.get_additional_filter_kwargs(*args, **kwargs))

    def get_additional_filter_kwargs(self, *args, **kwargs):
        """
        Method for generating a dict of additional keyword args to be used
        as filters on the queryset prior to pagination.
        Takes all the *args and **kwargs that get passed to get_context.
        """
        return {}

    def get_paginator_class(self):
        """
        Returns the class to use for pagination

        :return: Paginator class
        """
        return self.paginator_class

    def get_paginator_kwargs(self):
        """
        Method for generating a dict of keyword args that will be
        passed to the paginator constructor

        :param request: HttpRequest instance
        :return: Dict of keyword arguments to pass to the paginator class constructor
        """
        return {}

    def get_paginator(self, *args, **kwargs):
        """
        Returns a paginator instance

        :return: Paginator class
        """
        paginator_class = self.get_paginator_class()
        return paginator_class(*args, **kwargs)

    def paginate_queryset(self, queryset, page):
        """
        Helper method for paginating the queryset provided.

        :param queryset: Queryset of model instances to paginate
        :param page: Raw page number taken from the request dict
        :return: Queryset of child model instances
        """
        paginator = self.get_paginator(queryset, self.paginate_by, **self.get_paginator_kwargs())
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
        context = super(AbstractLibraryIndex, self).get_context(request, *args, **kwargs)
        queryset = children = self._get_children(request, *args, **kwargs)
        is_paginated = False
        paginator = None

        # Paginate the child nodes if paginate_by has been specified
        if self.paginate_by:
            is_paginated = True
            page_num = request.GET.get("page", 1) or 1
            children, paginator = self.paginate_queryset(children, page_num)

        context.update(
            queryset=queryset, children=children, paginator=paginator, is_paginated=is_paginated
        )
        return context


class AbstractLibraryDetail(Page):
    """Abstract library item detail page."""

    attachment = models.FileField(upload_to="attachments")
    content_panels = Page.content_panels + [FieldPanel("attachment")]

    class Meta(object):
        """Django properties."""

        abstract = True
