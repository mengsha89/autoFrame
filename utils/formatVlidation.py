# coding=utf-8
# author:ss

import json


def check_json_format(raw_msg):
    """
    用于判断一个字符串是否符合json格式
    :param raw_msg:
    :return:
    """
    # if isinstance(raw_msg, str):
    try:
        json.loads(raw_msg, encoding="utf-8")
    except ValueError:
        return False
    return True
    # else:
    #     return False
