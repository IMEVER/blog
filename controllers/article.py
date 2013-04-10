#!/usr/bin/env python
# -*- coding: utf-8 -*-

import web
import traceback
import config.settings as settings
import lib.utils as utils
import json

T_ARTICLE = 'article' #article table name

db = settings.db
render = settings.render

class Article:
  def GET(self):
    try:
      post_id = int(web.input(id = '0').id)
      myVar = dict(id=post_id)
      if post_id == 0:
        return render.error()
      post = db.select(T_ARTICLE,myVar, where="id=$id",limit = 1)
      ne_post = db.select(T_ARTICLE, myVar, where="id > $id",limit = 1)
      pre_post = db.select(T_ARTICLE, myVar, where='id < $id', limit = 1, order='date DESC')
      if len(post) == 0:
        return render.error()
      if len(pre_post) == 0:
        pre_post_id = 0
      else:
        pre_post_id = pre_post[0].id
      if len(ne_post)==0:
        ne_post_id = 0
      else:
        ne_post_id = ne_post[0].id
      return render.post(post[0], pre_post_id, ne_post_id, web.cookies())
    except:
      print 'exception when getting post'
      print traceback.format_exc()
      return render.error()


#return recommend article list limit 10 by json format
class Recommend:
  def GET(self, num=10):
    query = db.select(T_ARTICLE, limit=num, order=' comment desc').list()
    web.header('Content-Type', 'application/json')
    return json.dumps({'status':1, 'data': query}, cls=utils.ExtendedEncoder)
