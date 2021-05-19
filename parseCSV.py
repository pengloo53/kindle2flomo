import json
import requests

api = 'https://flomoapp.com/iwh/MzIzNQ/70306b07dbfe6d7be19a17c02e35592a/'

with open('files/Kindle-Notebook.csv', encoding='utf8') as file:
    result = []
    for index, line in enumerate(file):
        if index == 1:
            desc_index = line.find('（')
            if desc_index == -1:
                title = line[1:]
            else:
                title = line[1: desc_index]
        if index == 2:
            author = line
        if line[1:3] == '标注':
            highlight = line.split(',')[3][1:-2]
            result.append('#kindle/' + title + '\n标注：' + highlight)
        if line[1:3] == '笔记':
            note = line.split(',')[3][1:-2]
            result.append(result.pop() + '\n\n笔记：' + note)
    for content in result:
        s = json.dumps({'content': content})
        headers = {
            'Content-Type': 'application/json; charset=UTF-8'
        }
        r = requests.post(api, data=s, headers=headers)
