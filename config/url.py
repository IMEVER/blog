#!/usr/bin/env python
# coding: utf-8
import web
from config.admin_url import admin_urls

admin_app = web.application(admin_urls, locals())

pre_fix = 'controllers.pblog.'
comment_prefix = 'controllers.comment.'

urls = (
  '/(.*)/', pre_fix + 'Redirect',
  '/(favicon.ico)', pre_fix + 'Static',
  '/',  pre_fix + 'Index',
  '/post', pre_fix + 'Post',
  '/comment', comment_prefix + 'Comment',
  '/comment/add', comment_prefix + 'Comment',
  '/comment/vote', comment_prefix + 'Vote',
  '/tag', pre_fix + 'Tag',
  '/about',pre_fix + 'About',
  '/author/(.*)', pre_fix + 'Author',
  '/admin',admin_app, 
)
