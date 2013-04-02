#!/usr/bin/env python
# -*- coding: utf-8 -*-

import web
import sys
import md5
import random
import traceback
from config import settings
import json

T_ARTICLE = 'article'
T_COMMENT = 'comment'
T_MSG = 'msg'
T_USER = 'user'
T_TAG = 'tag'

render = settings.render
db = settings.db
reload(sys)
sys.setdefaultencoding("utf-8")

#def article

class Index:
  def GET(self):
    try:
      return render.error()
    except:
      print traceback.format_exc()
      return render.error()

class Vote:
  def GET(self):
    try:
      post_id = int(web.input(id = '0').id)
      myVar = dict(id=post_id)
      post = db.select(T_ARTICLE,myVar, where="id=$id",limit = 1)
      comments = db.select(T_COMMENT,myVar, where="articleid=$id");
      pre_post = db.select(T_ARTICLE, myVar, where='id < $id', limit = 1, order='date DESC')
      return render.post(post[0], pre_post_id, ne_post_id, len(comments), comments)
    except:
      print 'exception when getting post'
      print traceback.format_exc()
      return render.error()
    
  def POST(self):
    user_data = web.input()
    cid = int(user_data.get('cid', '-1'))
    dir = user_data.get('dir', False)
    
    web.header('Content-Type', 'application/json')
    if cid == -1 or dir == False:
      return json.dumps({'status':-1,'msg':'params error'})
    if dir == 'inc':
      db.update(T_COMMENT, where='id=$cid', upnum=web.sqlliteral('upnum+1'), vars=dict(cid=cid))
    elif dir == 'dec':
      #db.update(T_COMMENT, where='id=$cid', downnum='downnum-1', vars=dict(cid=cid))
      db.query("update comment set downnum = downnum+1 where id=$cid",vars=dict(cid=cid))
    return json.dumps({'status':1,'msg':'OK'})
