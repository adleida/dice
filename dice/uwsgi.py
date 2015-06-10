#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# File Name: dice/uwsgi.py
# Author: Tate_fan
# mail: tate_fan@163.com
# Created Time: 2015年06月05日 星期五 15时53分13秒
# ======================================================================
import dice
import logging
import logging.config
from .flask_app import WebApp, args, cfg
from .utils import get_res_path
from .schemasstore import SchemasStore
from .datagenerator import DataGenerator

logger = logging.getLogger(__name__)


# setting for logger
log = cfg.get('logging', {})
log.setdefault('version', 1)
logging.config.dictConfig(log)

debug = cfg.get("debug", False)
host = cfg.get("bind", '127.0.0.1')
webapp = WebApp()
