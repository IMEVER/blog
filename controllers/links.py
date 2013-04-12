#!/usr/bin/env python
# -*- encoding: utf8 -*-

import web
import json
import config.settings as settings

db = settings.db

T_LINKS = 'links'

class Links:
	def GET(self):
		data = db.select(T_LINKS, what="title,url,`desc`",  where="status=1", limit=10).list()
		
		web.header('Content-Type', 'application/json')
		return json.dumps({'status':1, 'data':data})

