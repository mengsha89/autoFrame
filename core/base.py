# coding=utf-8
# author:ss

import requests
from utils.log import Logger
import json
import traceback
from utils.formatVlidation import check_json_format

log = Logger()

# requests.adapters.DEFAULT_RETRIES = 5


class BaseApi(object):
    def __init__(self, url, header=None):
        self.header = header
        self.url = url

    def send_request(self, method, data=None, cookies=None):
        try:
            if method == "get":
                req = requests.get(self.url, headers=self.header, params=data, cookies=cookies)
            elif method == "post":
                if self.header is not None and self.header.get("Content-Type") == "application/json":
                    req = requests.post(self.url, headers=self.header, json=data, cookies=cookies)
                else:
                    req = requests.post(self.url, headers=self.header, data=data, cookies=cookies)
            if check_json_format(req.text):
                msg = "url:%s \n response:%s" % (self.url, json.dumps(req.json()).decode("unicode-escape"))
                log.info(msg)
                return req.json()
            else:
                msg = "url:%s \n response:%s" % (self.url, req.text)
                log.info(msg)
                return req.text

        except Exception:
            msg = "url:%s \n data:%s \n error info:%s" % (self.url, data, traceback.format_exc())
            log.error(msg)
