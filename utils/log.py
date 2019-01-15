# coding=utf-8
# author:ss

import logging
import config
import os
import datetime


class Logger(object):
    def __init__(self):
        clevel = config.clevel
        flevel = config.flevel
        self.log_dir = config.log_file_dir

        filename = 'auto_' + datetime.datetime.now().strftime('%Y%m%d') + '.log'
        if os.path.exists(self.log_dir):
            log_file = os.path.join(self.log_dir, filename)
        else:
            os.mkdir(r'%s' % self.log_dir)
            log_file = os.path.join(self.log_dir, filename)
        self.logger = logging.getLogger(__file__)
        if not self.logger.handlers:
            self.logger.setLevel(logging.DEBUG)
            # 定义日志输出格式
            fmt = logging.Formatter('[%(asctime)s]-[%(levelname)s]-%(message)s', '%Y-%m-%d %H:%M:%S')
            # 添加控制台输出：clevel对应级别及以上
            sh = logging.StreamHandler()
            sh.setLevel(clevel)
            sh.setFormatter(fmt)
            self.logger.addHandler(sh)
            # 添加日志文件输出：flevel对应级别及以上
            fh = logging.FileHandler(log_file)
            fh.setLevel(flevel)
            fh.setFormatter(fmt)
            self.logger.addHandler(fh)

    def cri(self, message):
        self.logger.critical(message)

    def error(self, message):
        self.logger.error(message)

    def warn(self, message):
        self.logger.warn(message)

    def info(self, message):
        self.logger.info(message)

    def debug(self, message):
        self.logger.debug(message)


logger = Logger()