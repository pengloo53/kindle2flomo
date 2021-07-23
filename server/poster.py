# 作者：鲁鹏
# Kindle 笔记导入 flomo
# 内容：批量导入 & 单条导入

import json
import time
import requests


def format_data_to_content(data, order):
    if order == 'up':
        if "note" in data:
            content = data["tag"] + '\n' + data["highlight"] + '\n' + data["delimiter"] + '\n<b>' + data["note"] + '</b>'
        else:
            content = data["tag"] + '\n' + data["highlight"]
    return content


def post_to_flomo(content, api):
    s = json.dumps({'content': content})
    headers = {
        'Content-Type': 'application/json; charset=UTF-8'
    }
    return requests.post(api, data=s, headers=headers)


# def post_all_to_flomo(json_data, api, is_order):
#     # 顺序查看，那么需要倒序插入笔记
#     if is_order:
#         json_data.reverse()
#     for index, content in enumerate(json_data):
#         s = json.dumps({'content': content})
#         headers = {
#             'Content-Type': 'application/json; charset=UTF-8'
#         }
#         r = requests.post(api, data=s, headers=headers)
#         # 需要顺序查看，才等待1s，保证页面效果
#         if is_order:
#             time.sleep(1)
#     return {
#         "code": 0,
#         "message": "总共 " + str(len(json_data)) + " 条，全部导入完成。"
#     }



