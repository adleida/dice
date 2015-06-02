#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# File Name: dice/dice.py
# Author: Tate_fan
# mail: tate_fan@163.com
# Created Time: 2015年06月01日 星期一 15时30分46秒
# ======================================================================
from .flask_app import WebApp
from .utils import get_res_path
import dice


def main():
    webapp = WebApp()
    webapp.run(debug=True)


if __name__ == '__main__':
    main()
