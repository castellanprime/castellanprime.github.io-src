#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Okusanya Oluwadamilola'
SITENAME = 'Thoughts of a software developer journeyman'
SITEURL = ''
THEME = 'themes/plumage'

PATH = 'content'
PLUGIN_PATHS = ['pelican-plugins']
PLUGINS = ['pelican_youtube', 'pelican_gist', 'pelican_comment_system',
	'series', 'just_table', 'better_code_samples',
	'render_math', 'pelican_javascript']

TIMEZONE = 'America/Chicago'

DEFAULT_LANG = 'en'

STATIC_PATHS=['images', 'files', 'extra/favicon.ico']

EXTRA_PATH_METADATA = {'extra/favicon.ico': {'path': 'favicon.ico'},}

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Github', 'https://github.com/castellanprime'),)

# Social widget
SOCIAL = (('LinkedIn', 'https://www.linkedin.com/in/oookusanya'),)

DEFAULT_PAGINATION = 8

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
