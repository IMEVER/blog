#!/usr/bin/env python
# -*- coding: utf-8 -*-

import traceback
import config.settings as settings

db = settings.db
render = settings.render

T_ARTICLE = 'article'
T_USER = 'user'

class Author:
  def GET(self,uid):
	try:
	  uid = int(uid)
	  myVar = dict(id=uid)
	  user = db.select(T_USER,myVar,where='id=$id',limit='1')
	  if len(user):
	    user = user[0]
	    posts = db.select(T_ARTICLE,myVar,where='usrid=$id',order='date DESC')
	  else:
	    user = {}
	    posts = {}
	  return render.author(user,posts)
    	except:
      	  print traceback.format_exc()
	  return render.error()  

