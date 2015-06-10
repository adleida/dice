#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# File Name: dice/utils.py
# Author: Tate_fan
# mail: tate_fan@163.com
# Created Time: 2015年06月01日 星期一 17时12分39秒
# ======================================================================
import requests
import json
import os
import yaml
import io
import pkgutil
import functools
import logging
import argparse
import dice
import os.path as _path
from faker import Factory


def json_dump(data):
    return json.dumps(data, indent=2)


@functools.lru_cache()
def load_resource(name, as_object=True):

    path = 'res/{}'.format(name)
    blob = pkgutil.get_data(__package__, path)
    if blob is None:
        raise Exception('no such resource: {}'.format(name))
    data = blob.decode()
    if as_object:
        ext = os.path.splitext(name)[-1]
        if ext in ['.json']:
            data = json.loads(data)
        elif ext in ['.yaml', '.yml']:
            data = yaml.load(io.StringIO(data))
        else:
            raise Exception('cannot detect resource type')
    return data


def init_args():

    arg_tmp = argparse.ArgumentParser()
    arg_tmp.add_argument('-v', '--version', action='version',
                         version=dice.__version__)
    arg_tmp.add_argument('-p', '--port', type=int, default=6060,
                         help='run app on port')
    arg_tmp.add_argument('-c', '--config', type=str, default='dice.yaml', help='config file')
    args = arg_tmp.parse_args()

    return args


def init_resource(url):
    try:
        return load_resource(url)
    except Exception:
        return requests.get(url).json()


def get_res_path(package, folder):
    if isinstance(package, str):
        package = __import__(package)
    return _path.join(_path.dirname(package.__file__), folder)


def make_fake_url(count):
    fake = Factory.create()
    count = count or 1
    return [fake.url() for _ in range(count)]
