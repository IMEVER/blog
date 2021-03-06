#!/usr/bin/env python
# -*- coding: utf-8 -*-

import web
from config.url import urls

app = web.application(urls,locals())

session = web.session.Session(app, web.session.DiskStore('userinfo'),initializer={'id':0,"seed":0,"hash":"",'user':'guest','uid':0})

def session_hook():
  web.ctx.session = session
  web.template.Template.globals['session'] = session

app.add_processor(web.loadhook(session_hook))
if __name__=="__main__":
  app.run()
