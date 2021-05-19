# 作者：鲁鹏
# Kindle 笔记导入 flomo
# 内容：批量导入 & 单条导入

import json
import time
import requests


def format_data_to_json(data_list, delimiter):
    result_json = []
    for data in data_list:
        if "note" in data:
            content = data["tags"] + '\n' + data["highlight"] + '\n' + delimiter + '\n笔记：' + data["note"]
        else:
            content = data["tags"] + '\n' + data["highlight"]
        result_json.append(content)
    return result_json


def post_all_to_flomo(json_data, api, is_order):
    # 顺序查看，那么需要倒序插入笔记
    if is_order:
        json_data.reverse()
    for index, content in enumerate(json_data):
        s = json.dumps({'content': content})
        headers = {
            'Content-Type': 'application/json; charset=UTF-8'
        }
        r = requests.post(api, data=s, headers=headers)
        # 需要顺序查看，才等待1s，保证页面效果
        if is_order:
            time.sleep(1)
    return {
        "code": 0,
        "message": "总共 " + str(len(json_data)) + " 条，全部导入完成。"
    }


def post_data_to_flomo(data, api):
    s = json.dumps({'content': data})
    headers = {
        'Content-Type': 'application/json; charset=UTF-8'
    }
    return requests.post(api, data=s, headers=headers)
