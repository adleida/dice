#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# File Name: dice/flask_api.py
# Author: Tate_fan
# mail: tate_fan@163.com
# Created Time: 2015年06月01日 星期一 16时40分13秒
# ======================================================================
import random
import time
import argparse
import requests
from . utils import load_resource, init_args, init_resource
from flask import Flask, request, jsonify,\
    current_app as app
from flask_restful import Resource, Api
from copy import deepcopy
import logging

logger = logging.getLogger(__name__)


class Bid(Resource):

    def post(self, did):
        if request.json:
            did_id = app.did_id(did)
            dd = deepcopy(app.ss.schemas)
            app.dg.schemas_store.schemas = dd
            adunit = request.json.get('adunit', {})

            count = adunit['param']['count']
            floor = adunit['floor']
            bid_unit = dd['bid_unit'][1]
            bid_response = dd['bid_response'][1]

            bid_unit['properties']['price']['minimum'] = floor
            bid_response['properties']['adm']['minItems'] = 1
            bid_response['properties']['adm']['maxItems'] = count
            del dd, bid_unit, bid_response

            tmp = app.dg.random_value('bid_response')
            sample = random.sample(did_id, len(tmp['adm']))
            for ids, item in zip(sample, tmp['adm']):
                item['id'] = ids
            tmp['nurl'] = app.make_rul(did)
            logging.info("Generate data: %s" % tmp)
            return tmp
        return app.dg.random_value('bid_response')


class Notice(Resource):

    def post(self, did):
        logging.info(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        logging.info("bid_notice: %s&%s", *(did, request.json))
        res = {"timestamp": time.time(), "message": "{did} get notice".format(did=did)}
        logging.info("res_notice: %s&%s", *(did, res))
        logging.info("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
        return res
