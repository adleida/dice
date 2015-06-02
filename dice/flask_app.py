#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# File Name: dice/flask_app.py
# Author: Tate_fan
# mail: tate_fan@163.com
# Created Time: 2015年06月01日 星期一 16时48分09秒
# ======================================================================
from flask import Flask
from . flask_api import Bid
from flask_restful import Api


class WebApp(Flask):

    def __init__(self, **kwargs):
        name = kwargs.pop("name", __package__)
        super(WebApp, self).__init__(name, **kwargs)
        self.init_rule()

    def run(self, host=None, port=None, debug=False, **options):
        super(WebApp, self).run(host, port, debug, **options)

    def init_rule(self):
        api = Api(self)
        api.add_resource(Bid, '/v1/bid/<string:did>')
