# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.ext import ndb
from graphapiclone.model import User, all_nodes, all_arcs


def index(_write_tmpl):
    values = {'nodes': all_nodes.keys(), 'arcs': all_arcs.keys()}
    _write_tmpl('templates/home.html', values)


def setup():
    def setup_models(model_cls):
        model_count = model_cls.query().count(1)
        if model_count == 0:
            return [model_cls(name=model_cls.type + str(i)) for i in xrange(3)]
        return []

    models = setup_models(User)

    if models:
        ndb.put_multi(models)


