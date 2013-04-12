#!/usr/bin/env python
# coding: utf-8
import web
from config.admin_url import admin_urls

admin_app = web.application(admin_urls, locals())

pre_fix = 'controllers.pblog.'
comment_prefix = 'controllers.comment.'
about_prefix = 'controllers.about.'
article_prefix = 'controllers.article.'
author_prefix = 'controllers.author.'
links_prefix = 'controllers.links.'

urls = (
  '/(.*)/', pre_fix + 'Redirect',
  '/(favicon.ico)', pre_fix + 'Static',
  '/',  pre_fix + 'Index',
  '/post', pre_fix + 'Post',
  '/article', article_prefix + 'Article',
  '/article/recommend', article_prefix + 'Recommend',
  '/comment', comment_prefix + 'Comment',
  '/comment/add', comment_prefix + 'Comment',
  '/comment/vote', comment_prefix + 'Vote',
  '/tag', pre_fix + 'Tag',
  '/about',about_prefix + 'About',
  '/author/(.*)', author_prefix + 'Author',
  '/links', links_prefix + 'Links',
  '/admin',admin_app, 
)
