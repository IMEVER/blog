#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import hashlib, urllib
import socket, struct
import json

#translate ip from string to num
def ip2long(ip):
        return struct.unpack("!I",socket.inet_aton(ip))[0]

#translate ip from num to string
def long2ip(ip):
        return socket.inet_ntoa(struct.pack("!I",ip))

#get avatar from gravatar.com by email
def getAvatarUrl(email):
        default = "http://www.imever.cn:8080/static/images/gravatar.png"
        size = 40
        
        gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?"
        #gravatar_url += urllib.urlencode({'d':default,'s':str(size)})

        gravatar_url += urllib.urlencode({'d':'mm', 's':str(size)})
        return gravatar_url

#extend jsonEncoder to solve datetime problem
class ExtendedEncoder(json.JSONEncoder):
  def default(self, o):
    if isinstance(o,datetime.datetime):
      return o.strftime("%Y-%m-%d %H:%M:%S")
    return json.JSONEncoder(self, o)

