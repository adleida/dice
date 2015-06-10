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
from . utils import load_resource, init_args, init_resource, make_fake_url
from flask import Flask, request, jsonify, abort,\
    current_app as app
from flask_restful import Resource, Api
from copy import deepcopy
import logging
import json
import dice

logger = logging.getLogger(__name__)


class Bid(Resource):

    def post(self, did):
        if request.json:
            logging.info(request.data)
            start = time.clock()
            did_id = app.did_id(did)
            if not did_id:
                abort(404)
            dd = deepcopy(app.ss.schemas)
            app.dg.schemas_store.schemas = dd
            adunit = request.json.get('adunit', {})

            count = adunit['param']['count']
            floor = adunit['floor']
            bid_unit = dd['bid_unit'][1]
            bid_response = dd['bid_response'][1]

            if count > len(did_id):
                count = len(did_id)

            bid_unit['properties']['price']['minimum'] = floor
            bid_response['properties']['adm']['minItems'] = 1
            bid_response['properties']['adm']['maxItems'] = count
            del dd, bid_unit, bid_response

            tmp = app.dg.random_value('bid_response')
            sample = random.sample(did_id, len(tmp['adm']))
            for ids, item in zip(sample, tmp['adm']):
                item['id'] = ids
            tmp['nurl'] = app.make_rul(did)
            tmp['id'] = request.json.get("id", "")
            tmp['did'] = did

            for item in tmp['adm']:
                if 'tracking_url' in item:
                    item['tracking_url'] = make_fake_url(len(item['tracking_url']))
                if 'click_through_url' in item:
                    item['click_through_url'] = make_fake_url(len(item['click_through_url']))

            logging.info("===============================================")
            logging.info("Generate data: %s" % tmp)
            logging.info("===============================================")
            end = time.clock()
            logging.info("Escaped time: %s" % (end - start))
            return tmp
        abort(403)


class Root(Resource):
    def get(self):
        return {
            "Message": "WELCOME TO AD DICE",
            "time stamp": time.time(),
            "version": dice.__version__
        }


class Notice(Resource):

    def post(self, did):
        logging.info(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        logging.info("bid_notice: %s&%s", *(did, request.json))
        res = {"timestamp": time.time(), "message": "{did} get notice".format(did=did)}
        logging.info("res_notice: %s&%s", *(did, res))
        logging.info("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
        return res
