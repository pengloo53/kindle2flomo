# 作者：鲁鹏
# Kindle 笔记导入 flomo
# 内容：批量导入 & 单条导入

import json
import time
import requests


def format_data_to_content(data, order):
    if order == 'up':
        if data['note']:
            content = data["tag"] + '\n' + data["highlight"] + '\n' + data["delimiter"] + '\n笔记：' + data["note"]
        else:
            content = data["tag"] + '\n' + data["highlight"]
    elif order == 'down':
        if data['note']:
            content = data["highlight"] + '\n' + data["delimiter"] + '\n笔记：' + data["note"] + '\n' + data['tag']
        else:
            content = data["highlight"] + '\n' + data['tag']
    return content


def post_to_flomo(content, api):
    s = json.dumps({'content': content})
    headers = {
        'Content-Type': 'application/json; charset=UTF-8'
    }
    r = requests.post(api, data=s, headers=headers)
    return json.loads(r.text)



