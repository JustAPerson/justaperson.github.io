#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Jason Priest'
SITENAME = 'Pursuing Fast'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'EST'

DEFAULT_LANG = 'en'

THEME = './theme/'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

MENUITEMS = [
    ("About", "/"),
    ("Experience", "/about/experience/"),
    ("Projects", "/about/projects/"),
    ("Classwork", "/about/classwork/"),
    ("Resume", "/pdfs/jpriest_resume_fall_2018.pdf"),
]

# Blogroll
LINKS = ()
# LINKS = (('Pelican', 'http://getpelican.com/'),
#          ('Python.org', 'http://python.org/'),
#          ('Jinja2', 'http://jinja.pocoo.org/'),
#          ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (("GitHub", "https://github.com/JustAPerson/"),
          ("Email", "mailto:jpriest@mit.edu"),)

DEFAULT_PAGINATION = 10


STATIC_PATHS = ['pdfs', 'extra']
EXTRA_PATH_METADATA = {
    'extra/favicon_0x7A_bwout_nocorner.png': {'path': 'favicon.png'}
}

DISPLAY_PAGES_ON_MENU = False
DISPLAY_CATEGORIES_ON_MENU = False

PAGE_PATHS = ['pages', 'wiki']
PAGE_URL="{slug}"
PAGE_SAVE_AS=PAGE_URL + "/index.html"

PLUGIN_PATHS = ["./plugins/"]
# PLUGINS = ["extract_toc"]

MARKDOWN = {
    'extension_configs': {
        'markdown.extensions.codehilite': {'css_class': 'highlight'},
        # 'markdown.extension.attr_list': {}, # https://python-markdown.github.io/extensions/attr_list/
        'markdown.extensions.extra': {},
        'markdown.extensions.meta': {},
        # 'markdown.extensions.headerid': {},
        'markdown.extensions.wikilinks': {'base_url': '/wiki/'},
        'markdown.extensions.toc': {},
        'markdown.extensions.sane_lists': {},
    },
    'output_format': 'html5',
}

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

# DEFAULT_METADATA = {
#     'status': 'draft',
# }
