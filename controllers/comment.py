#!/usr/bin/env python
# -*- coding: utf-8 -*-

import web
import sys
import md5
import random
import traceback
from config import settings
import json
import datetime
import socket
import struct
import urllib, hashlib

T_ARTICLE = 'article'
T_COMMENT = 'comment'
T_COMMENT_VOTE = 'comment_vote'
T_MSG = 'msg'
T_USER = 'user'
T_TAG = 'tag'

render = settings.render
db = settings.db
reload(sys)
sys.setdefaultencoding("utf-8")

def ip2long(ip):
	return struct.unpack("!I",socket.inet_aton(ip))[0]

class ExtendedEncoder(json.JSONEncoder):
  def default(self, o):
    if isinstance(o,datetime.datetime):
      return o.strftime("%Y-%m-%d %H:%M:%S")
    return json.JSONEncoder(self, o)

def getAvatarUrl(email):
        default = "http://www.imever.cn:8080/static/images/gravatar.png"
        size = 40
        
        gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?"
        #gravatar_url += urllib.urlencode({'d':default,'s':str(size)})

        gravatar_url += urllib.urlencode({'d':'mm', 's':str(size)})
        return gravatar_url


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
    if cid == -1 or dir == False or (dir != 'inc' and dir != 'dec'):
      return json.dumps({'status':-1,'msg':'params error'})

    ip = ip2long(web.ctx['ip'])
    useragent = web.ctx.env['HTTP_USER_AGENT']
    author = web.cookies().author
    email = web.cookies().email
    votes = db.select(T_COMMENT_VOTE, dict(id=cid,ip=ip), where="cid=$id and ipv4=$ip")
    if len(votes):
        return json.dumps({'status':0,'msg':'You have already voted'})
    if dir == 'inc':
      db.update(T_COMMENT, where='id=$cid', upnum=web.sqlliteral('upnum+1'), vars=dict(cid=cid))
    elif dir == 'dec':
      db.query("update comment set downnum = downnum+1 where id=$cid",vars=dict(cid=cid))
    db.insert(T_COMMENT_VOTE, id=0, date=web.SQLLiteral("NOW()"), dir=dir, email = email, cid = cid, author = author, ipv4 = ip, useragent = useragent)
    return json.dumps({'status':1,'msg':'OK'})

class Comment:
  def GET(self):
    post_id = int(web.input(id='0').id)
    web.header('Content-Type', 'application/json')
    if post_id == 0:
      return json.dumps({'status':0, 'msg':'Param error'})
    myVar = dict(id=post_id)
    comments = db.select(T_COMMENT,myVar, where="articleid=$id").list();
    for comment in comments:
      comment.head = getAvatarUrl(comment.email)
    return json.dumps({'status':1, 'data':comments}, cls=ExtendedEncoder)

  def POST(self):
    user_data = web.input()
    author = user_data.get('author', '')
    email = user_data.get('email', '')
    website = user_data.get('website', '')
    post_id = int(user_data.get('post_id', '-1'))
    content = user_data.get('content', '')    

    web.header('Content-Type', 'application/json')
    if post_id == -1:
      return json.dumps({'status':0, 'msg':'params error'})
    ip = ip2long(web.ctx['ip'])
    useragent = web.ctx.env['HTTP_USER_AGENT']

    insert_id = db.insert(T_COMMENT, id=0, date=web.SQLLiteral("NOW()"), homepage=website, email = email, articleid = post_id, content = content, author = author, ipv4 = ip, useragent = useragent)
    age = 30*24*60*60
    web.setcookie('email',email,age)
    web.setcookie('author',author,age)
    web.setcookie('website','website',age)
    #web.seeother('/post?id=' + user_data.get('post_id', ''))
    return json.dumps({'status':1, 'msg':'Success','cid':insert_id})

