#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
import os

DEBUG = bool(int(os.environ.get('DEBUG', '1')))

AUTHOR = os.environ.get('PELICAN_AUTHOR', 'unknown')

SITENAME = os.environ.get('PELICAN_SITENAME', 'Pelican Blog')


if DEBUG:
    SITEURL = 'http://localhost:8079'
else:
    SITEURL = os.environ.get('PELICAN_SITEURL', 'http://localhost')

TIMEZONE = 'Europe/London'

DEFAULT_LANG = 'en'

BASEDIR = os.path.dirname(os.path.abspath(__file__))

PATH = BASEDIR
PAGE_PATHS = ['pages']
ARTICLE_PATHS = ['articles']
ARTICLE_EXCLUDES = ['img']

USE_FOLDER_AS_CATEGORY = True
ARTICLE_URL = 'blog/{category}/{slug}/'
ARTICLE_SAVE_AS = 'blog/{category}/{slug}/index.html'
PAGE_URL = '{slug}/'
PAGE_SAVE_AS = '{slug}/index.html'
CATEGORY_URL = 'blog/{slug}/'
CATEGORY_SAVE_AS = 'blog/{slug}/index.html'
CATEGORIES_SAVE_AS =  'blog/index.html'
TAG_URL = 'blog/list/tag/{slug}/'
TAG_SAVE_AS = 'blog/list/tag/{slug}/index.html'
TAGS_SAVE_AS =  'blog/list/tag/index.html'
AUTHOR_URL = 'blog/list/author/{slug}/'
AUTHOR_SAVE_AS = 'blog/list/author/{slug}/index.html'
AUTHORS_SAVE_AS =  'blog/list/author/index.html'
ARCHIVES_SAVE_AS =  'blog/list/archive/index.html'

THEME = os.path.join(PATH, 'theme')
THEME_STATIC_DIR = 'assets'
THEME_STATIC_PATHS = ['static']

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

DEFAULT_PAGINATION = 20

PLUGIN_PATHS = [
    os.path.join(BASEDIR, 'plugins'),
]
PLUGINS = [
    'youtube', 'sitemap', 'jsfiddle', 'render_math',
]

SITEMAP = {
    'format': 'xml',
}
# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
