#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/4/17 9:52
# @Author  : Fred Yangxiaofei
# @File    : startup.py
# @Role    : 启动脚本


import fire
from tornado.options import define
from websdk.program import MainProgram
from settings import settings as app_settings
from biz.applications import Application as CmdbApp
from biz.crontab_app import Application as CronApp


define("service", default='api', help="start service flag", type=str)


class MyProgram(MainProgram):
    def __init__(self, service='cmdb_api', progress_id='cmdb'):
        self.__app = None
        settings = app_settings
        if service == 'cmdb':
            self.__app = CmdbApp(**settings)
        elif service == 'cron_app':
            self.__app = CronApp(**settings)
        super(MyProgram, self).__init__(progress_id)
        self.__app.start_server()


if __name__ == '__main__':
    fire.Fire(MyProgram)
