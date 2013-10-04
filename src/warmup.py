# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import sys

import os

#Put lib on path, once Google App Engine does not allow doing it directly
sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))

import webapp2


class BaseHandler(webapp2.RequestHandler):
    def get(self):
        pass




app = webapp2.WSGIApplication([("/.*", BaseHandler)], debug=False)

