#! /usr/bin/env python
# -*- coding: utf-8 -*-

import web
import os

web.config.debug = True
db = web.database(dbn='mysql', db='blog',user='root',pw='')
render = web.template.render('tpls/',base="layout")
post_content = web.template.render('tpls/')
admin_render = web.template.render('tpls/admin-tpls')
config = web.storage(
    email = 'linyetian@gmail.com',
    site_name = 'IMEVER\'s Blog',
    static = '/static',
    description='A Simple Python Blog',
    author='Rhett Tian',
)
image_upload_dir = os.path.dirname(os.path.abspath(__file__)) + r"/../static/upload/imgs/"
file_upload_dir = os.path.dirname(os.path.abspath(__file__)) + r"/../static/upload/"
web.template.Template.globals['config'] = config
web.template.Template.globals['render'] = post_content
###web.template.Template.globals['session'] = web.ctx.session
