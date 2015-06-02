#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# File Name: dice/flask_app.py
# Author: Tate_fan
# mail: tate_fan@163.com
# Created Time: 2015年06月01日 星期一 16时48分09秒
# ======================================================================
import logging
from flask import Flask
from . flask_api import Bid, Notice
from flask_restful import Api
from .utils import get_res_path, init_args,\
    load_resource, init_resource
from .datagenerator import DataGenerator
from .schemasstore import SchemasStore
args = init_args()
cfg = load_resource(args.config)
logger = logging.getLogger(__name__)


class WebApp(Flask):

    def __init__(self, resource=None, **kwargs):
        self.dg = DataGenerator()
        self.ss = SchemasStore()
        self.resource = resource or [{}]
        self.port = args.port or 6060
        name = kwargs.pop("name", __package__)
        super(WebApp, self).__init__(name, **kwargs)
        self.init_rule()
        self.init_schema()
        self.init_res()

    def run(self, host=None, debug=False, **options):
        super(WebApp, self).run(host=host, port=self.port, debug=debug, **options)

    def init_rule(self):
        api = Api(self)
        api.add_resource(Bid, '/v1/bid/<string:did>')
        api.add_resource(Notice, '/v1/notice/<string:did>')

    def init_schema(self, folder='res'):
        self.ss.load_folder(get_res_path(__package__, folder))
        self.dg.schemas_store = self.ss

    def init_res(self):
        url = cfg.get("resource")
        self.resource = init_resource(url)

    def did_id(self, did):
        return [item['id'] for item in self.resource if item['did'] == did]

    def make_rul(self, did):
        return "http://dsp:{port}/v1/notice/{did}".format(port=self.port, did=did)
