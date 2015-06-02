#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# File Name: dice/flask_api.py
# Author: Tate_fan
# mail: tate_fan@163.com
# Created Time: 2015年06月01日 星期一 16时40分13秒
# ======================================================================
import time
import argparse
import requests
from . utils import load_resource, init_args, init_resource
from flask import Flask, request, jsonify,\
    current_app as app
from flask_restful import Resource, Api

args = init_args()
cfg = load_resource(args.config)
url = cfg.get("resource")
ress = init_resource(url)


class Bid(Resource):

    def post(self, did):
        return ress


class Notice(Resource):

    def post(self, did):

        return {"timestamp": time.time()}
