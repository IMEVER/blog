#!/usr/bin/env python
# -*- coding: utf-8 -*-

import config.settings as settings

render = settings.render

class About:
  def GET(self):
    return render.about()
