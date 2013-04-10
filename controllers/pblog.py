#!/usr/bin/env python
# -*- coding: utf-8 -*-

import web
import sys
import traceback
from lib import utils
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
