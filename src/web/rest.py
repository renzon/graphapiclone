# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import json
from gaegraph.business_base import DestinationsSearch, NodeSearch
from gaegraph.model import Arc, to_node_key
from graphapiclone.model import all_arcs, all_nodes


def __extract_dct(node):
    node_dct = node.to_dict(exclude=['creation', 'class_', 'key'])
    node_dct['id'] = str(node.key.id())
    return node_dct


def getall(_resp, type):
    node_cls = all_nodes.get(type)
    nodes = node_cls.query().fetch()
    node_dct_list = [__extract_dct(n) for n in nodes]
    js = json.dumps(node_dct_list)
    _resp.write(js)


def find(_resp, id, arc=None):
    if arc:
        arc_cls = all_arcs.get(arc)
        destinations = DestinationsSearch(arc_cls, id).execute().result
        destination_dct_list = [__extract_dct(d) for d in destinations]
        js = json.dumps(destination_dct_list)
        _resp.write(js)
    else:
        node = NodeSearch(id).execute().result
        js = json.dumps(__extract_dct(node))
        _resp.write(js)


def setarc(_resp, arc, origin_id, destination_id):
    arc_cls = all_arcs.get(arc)
    arc_count = Arc.query(Arc.origin == to_node_key(origin_id), Arc.destination == to_node_key(destination_id)).count()
    if arc_count > 0:
        _resp.write("Arc already exists")
    else:
        arc_cls(origin=to_node_key(origin_id), destination=to_node_key(destination_id)).put()
        _resp.write("Arc Created")

