# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import json
import sys
import os

#Put lib on path, once Google App Engine does not allow doing it directly
sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))

import tmpl
import logging
import traceback
import webapp2
from zen import router
from zen.router import PathNotFound


def _extract_values(handler, param, default_value=""):
    values = handler.request.get_all(param)
    if param.endswith("[]"):
        return param[:-2], values if values else []
    else:
        if not values: return param, default_value
        if len(values) == 1: return param, values[0]
        return param, values


def execute_middlewares(midlewares, req, resp, handler_fcn):
    if midlewares:
        current_middleware = midlewares[0]

        def next_process():
            next_middlewares = midlewares[1:]
            execute_middlewares(next_middlewares, req, resp, handler_fcn)

        current_middleware(req, resp, next_process)
    else:
        handler_fcn()


class BaseHandler(webapp2.RequestHandler):
    def get(self):
        self.make_convetion()

    def post(self):
        self.make_convetion()

    def make_convetion(self):
        angular_ajax_accept = r'application/json, text/plain, */*'
        header_value = getattr(self.request, 'accept', None)
        header_value = getattr(header_value, 'header_value', None)
        if header_value == angular_ajax_accept and self.request.body:
            kwargs = json.loads(self.request.body)
        else:
            kwargs = dict(_extract_values(self, a) for a in self.request.arguments())

        def write_tmpl(template_name, values=None):
            values = values or {}
            return self.response.write(tmpl.render(template_name, values))

        convention_params = {"_req": self.request,
                             "_resp": self.response,
                             "_handler": self,
                             "_render": tmpl.render,
                             "_write_tmpl": write_tmpl}
        convention_params["_dependencies"] = convention_params
        try:
            fcn, params = router.to_handler(self.request.path, convention_params, **kwargs)
            fcn(*params, **kwargs)
        except PathNotFound:
            self.response.status_code = 404
            logging.error("Path not Found: " + self.request.path)


app = webapp2.WSGIApplication([("/.*", BaseHandler)], debug=False)

