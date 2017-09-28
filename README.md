# Wagtail Library [![Build Status](https://travis-ci.com/omni-digital/omni-wagtail-library.svg?token=9QKsFUYHUxekS7Q4cLHs&branch=master)](https://travis-ci.com/omni-digital/omni-wagtail-library)

A wagtail library for creating a library of documents or files for distribution from your website

## Requirements

Wagtail Library requires Django 1.10 or later and Wagtail 1.11 or later.

## Supported Versions

Python: 2.7, 3.4, 3.5, 3.6

Django: 1.10, 1.11

Wagtail: 1.11, 1.12

## Getting started

Installing from pip:

```
pip install wagtail-library
```

Adding to `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    ...
    'wagtail_library',
    ...
]
```

Running the migrations:

```
python manage migrate wagtail_library
```

## Models

### LibraryIndex

An index/listing page for library detail pages.

### LibraryDetail

A detail page for a library item

## Overriding pagination

If you decide to provide your own concrete implementation of the LibraryIndex (by subclassing AbstractLibraryIndex) you may override the pagination class.

The simplest way of achieving this is to assign your paginator class using the `paginator_class` attribute on your model.

More fine grained control can be achieved by overriding the following methods:

 - `get_paginator_class` - Should return the paginator class to be used by the listing page.  Returns `Model.paginator_class` (djangos core paginator class) by default
 - `get_paginator_kwargs` - If your custom paginator's constructor accepts extra keyword args this method can be overridden to provide them.  Returns a dictionary of keyword args to pass to the paginator constructor (An empty dictionary by default)
 - `get_paginator` - Accepts a queryset or iterable, page count (number of results per page) and any keyword arguments returned by `get_paginator_kwargs`. Should return a paginator instance.
 - `paginate_queryset` - Handles pagination of a queryset. Accepts a queryset or iterable, and the page number being requested. Returns a tuple: (PaginatorPage, Paginator)

## Warranty


*THIS SOFTWARE IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE. THE ENTIRE RISK AS TO THE USE OF THIS SOFTWARE IS WITH YOU.*

*IN NO EVENT WILL ANY COPYRIGHT HOLDER, OR ANY OTHER PARTY WHO MAY MODIFY AND/OR REDISTRIBUTE THE LIBRARY, BE LIABLE TO YOU FOR ANY DAMAGES, EVEN IF SUCH HOLDER OR OTHER PARTY HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.*
