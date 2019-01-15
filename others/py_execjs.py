# coding=utf-8
# author:ss


import execjs
import os
import time
import random
import config

# os.environ["NODE_PATH"] = os.getcwd() + "/node_modules"
os.environ["NODE_PATH"] = config.path + r"\resources\app\node_modules"


def get_js():
    print(os.getcwd())
    # file = os.getcwd() + r"\src\pages\client\red-bag\ag\index.js"
    file = config.path + r"\resources\app\node_modules"

    with open(file, "r") as f:
        line = f.readline()
        jsstr = " "
        while line:
            jsstr = jsstr + line
            line = f.readline()
    return jsstr


def exec_js_func(js, arg):
    # js = get_js()
    ctx = execjs.compile(js)
    return ctx.call("onPickBack", 0, arg)


if __name__ == '__main__':
    sid = random.randint(1, 5)
    ks = random.choice(["A", "B", "C", "D"])
    arg = {"iMode": 1, "iBaseID": sid, "sInfo": ks, "pick_time": int(round(time.time()*1000))}
    exec_js_func(arg)