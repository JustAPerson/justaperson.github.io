#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Jason Priest'
SITENAME = 'Pursuing Fast'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'EST'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

MENUITEMS = [
    ("Home", "/"),
    ("Wiki", "/wiki/"),
    ("Resume", "/pdfs/jpriest_resume_fall_2017.pdf"),
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


STATIC_PATHS = ['pdfs']

DISPLAY_PAGES_ON_MENU = False
DISPLAY_CATEGORIES_ON_MENU = False

PAGE_URL="{slug}.html"
PAGE_SAVE_AS=PAGE_URL

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

# DEFAULT_METADATA = {
#     'status': 'draft',
# }
