import datetime
try:
    import urllib.parse as urlparse
except ImportError:
    import urlparse

from django_jinja import library
from django.utils import six
from django.utils.encoding import smart_text
from django.utils.http import urlencode

import jinja2


@library.filter
def fe(s, *args, **kwargs):
    """Format a safe string with potentially unsafe arguments, then return a
    safe string."""
    s = six.text_type(s)
    args = [jinja2.escape(smart_text(v)) for v in args]
    for k in kwargs:
        kwargs[k] = jinja2.escape(smart_text(kwargs[k]))
    return jinja2.Markup(s.format(*args, **kwargs))


@library.global_function
def thisyear():
    """The current year."""
    return datetime.date.today().year


@library.filter
def urlparams(url_, hash=None, **query):
    """Add a fragment and/or query paramaters to a URL.

    New query params will be appended to exising parameters, except duplicate
    names, which will be replaced.
    """
    url = urlparse.urlparse(url_)
    fragment = hash if hash is not None else url.fragment

    # Use dict(parse_qsl) so we don't get lists of values.
    query_dict = dict(urlparse.parse_qsl(url.query))
    query_dict.update(query)

    query_string = urlencode(
        [(k, v) for k, v in query_dict.items() if v is not None])
    new = urlparse.ParseResult(url.scheme, url.netloc, url.path, url.params,
                               query_string, fragment)
    return new.geturl()
