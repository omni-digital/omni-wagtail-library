# Wagtail Library [![Build Status](https://travis-ci.com/omni-digital/omni-wagtail-library.svg?token=9QKsFUYHUxekS7Q4cLHs&branch=master)](https://travis-ci.com/omni-digital/omni-wagtail-library)

A wagtail package for a document library.

## Requirements

Wagtail Library requires Django 1.8 or later and Wagtail 1.8 or later.

## Supported Versions

Python: 2.7, 3.4, 3.5, 3.6

Django: 1.8, 1.9, 1.10, 1.11

Wagtail: 1.8, 1.9, 1.10, 1.11, 1.12

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

An index/listing page for LibraryDetail instances, with optional pagination.

### LibraryDetail

A detail page containing a document & information relating to the document.

##  Blocks

### LibraryDetailBlock

A streamfield block for adding links to LibraryDetail pages outside of the LibraryIndex.

## Warranty


*THIS SOFTWARE IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE. THE ENTIRE RISK AS TO THE USE OF THIS SOFTWARE IS WITH YOU.*

*IN NO EVENT WILL ANY COPYRIGHT HOLDER, OR ANY OTHER PARTY WHO MAY MODIFY AND/OR REDISTRIBUTE THE LIBRARY, BE LIABLE TO YOU FOR ANY DAMAGES, EVEN IF SUCH HOLDER OR OTHER PARTY HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.*


Again, see the included LICENSE file for specific legal details.
