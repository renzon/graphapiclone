# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.ext import ndb
from gaegraph.model import Node, Arc


class User(Node):
    type = 'user'
    name = ndb.StringProperty(required=True)


class Friend(Arc):
    type = 'friends'


class Album(Node):
    type = 'album'
    name = ndb.StringProperty(required=True)
    description = ndb.StringProperty(required=True)


class AlbumArc(Arc):
    type = 'albums'


arc_classes = [Friend, AlbumArc]
all_arcs = {arc.type: arc for arc in arc_classes}

all_node_classes = [User, Album]
all_nodes = {arc.type: arc for arc in all_node_classes}

all_nodes_and_arcs = dict(all_nodes)
all_nodes_and_arcs.update(all_arcs)
