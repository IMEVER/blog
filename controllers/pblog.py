#!/usr/bin/env python
# -*- coding: utf-8 -*-

import web
import sys
import md5
import random
import traceback
import urllib, hashlib
import socket
import struct
from config import settings



T_ARTICLE = 'article'
T_COMMENT = 'comment'
T_MSG = 'msg'
T_USER = 'user'
T_TAG = 'tag'

render = settings.render
db = settings.db
reload(sys)
sys.setdefaultencoding("utf-8")

def recommendList():
	query= db.select(T_ARTICLE,limit=10,where="comment>0",order="comment desc")
	posts = []
	for item in query:
		article={}
		article['id'] = item.id
		article['title'] = item.title
		posts.append(article)
	return posts
#print recommendList()

def getAvatarUrl(email):
	default = "http://www.imever.cn:8080/static/images/gravatar.png"
	size = 40
	
	gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?"
	#gravatar_url += urllib.urlencode({'d':default,'s':str(size)})

	gravatar_url += urllib.urlencode({'d':'mm', 's':str(size)})
	return gravatar_url

web.template.Template.globals['rList'] = recommendList()
web.template.Template.globals['getAvatarUrl'] = getAvatarUrl

def ip2long(ip):
	return struct.unpack("!I",socket.inet_aton(ip))[0]
def long2ip(ip):
	return socket.inet_ntoa(struct.pack("!I",ip))

#def article

class Redirect:
  def GET(self, path):
    web.seeother('/' + path)
class Static:
  def GET(self,path):
    #web.seeother('/static/' + path)
    web.header("Content-Type","image/x-icon")
    return open("static/"+path,"rb").read()


class Index:
  def GET(self):
    try:
      page = int(web.input(p = '1').p) - 1
      query = db.select(T_ARTICLE,limit="%d,5"%(page*5),order="date DESC")
      posts = []
      if len(query)==0 and page != 0:
        return render.error()

      for post in query:
        article = {}
        article['id'] = post.id
        article['date'] = post.date
        article['tags'] = post.tag
        article['title'] = post.title
        article['content'] = post.content
	article['usrid'] = post.usrid
	article['author'] = post.author
        c_count = int(db.query("select count(*) from " + T_COMMENT + " where articleid = $post_id", vars={"post_id":post.id})[0]["count(*)"])
        article['c_count'] = c_count
        print "post_id=%d,c_count:%d" % (post.id, article['c_count'])
        posts.append(article)

      count = int(db.query("select count(*) from " + T_ARTICLE)[0]["count(*)"])
      ne = pre = 0
      maxpage = count / 5
      
      if maxpage % 5 != 0:
        maxpage += 1

      if page > 0:
        pre = page

      if page+1 < maxpage:
        ne = page + 2
      return render.index(posts, ne, pre)
    except:
      print traceback.format_exc()
      return render.error()

class Post:
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
class About:
  def GET(self):
    return render.about()
    
class Tag:
  def GET(self):
    try:
      page = int(web.input(p = '1').p) - 1;
      tag_filted = web.input(key='').key
      if tag_filted == '':
        return render.error()
      query = db.select(T_ARTICLE, limit = "%d,5"%(page * 5), where="tag like '%"+tag_filted+"%'", order="date DESC")
      posts = []
      for post in query:
        article = {}
        article['id'] = post.id
        article['date'] = post.date
        article['tags'] = post.tag
        article['title'] = post.title
        article['content'] = post.content
	article['usrid'] = post.usrid
	article['author'] = post.author
        c_count = int(db.query("select count(*) from " + T_COMMENT + " where articleid = $post_id", vars={"post_id":post.id})[0]["count(*)"])
        article['c_count'] = c_count
        print "post_id=%d,c_count:%d" % (post.id, article['c_count'])
        posts.append(article)


      count = int(db.query("select count(*) from " + T_ARTICLE + " where tag like '%" + tag_filted +"%'")[0]["count(*)"])
      ne = pre = 0
      maxpage = count / 5
      if maxpage % 5 != 0:
        maxpage += 1
      if page > 0:
        pre = page
      if page+1 < maxpage:
        ne = page + 2
      return render.tag(tag_filted,posts, ne, pre);
    except:
      print traceback.format_exc()
      return render.error()
