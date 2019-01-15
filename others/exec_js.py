# coding=utf-8
# author:ss

import execjs
import json
import sys

reload(sys)

sys.setdefaultencoding("utf8")


def get_js():

    f = open("./core.v2.9.1.min.js", 'r')
    line = f.readline()
    htmlstr = ''
    while line:
        htmlstr = htmlstr + line
        line = f.readline()
    return htmlstr


jsstr = get_js()
ctx = execjs.compile(jsstr)
json_data = {"data":
        {"result": True,
        "token": "fd0d58f8752649d194f4d3963f431be3",
        "validate": "UUvWTvH49IYISN7n81g/P7i48efcAeePMm7g2LNwK2pjkdMeQ43xVpR1cHhwBYfZfro1N4adXW8JajKg3WW78aKiu44DUiySgc/6RhwiHGM6VwNXKZ+qP+4KmKJMpSt2uSBkBBqmOA7O0kHHYrLSUOkv4qN6KHcCV403s8qPBS0="},
        "error": 0,
        "msg": "ok"}
print(ctx.call("__JSONP_k9va8y8_1",json.dumps(json_data)))





