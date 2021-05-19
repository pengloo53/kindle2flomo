import json
from bs4 import BeautifulSoup
import requests

# api
api = 'https://flomoapp.com/iwh/MzIzNQ/70306b07dbfe6d7be19a17c02e35592a/'
# 分隔符
delimiter = '>>>>>>>>>'
# 文件路径
html_file_path = 'files/不拘一格：网飞的自由与责任工作法.html'


def open_html_file(file_path):
    result_arr = []     # HTML中有效数据
    result_json = []    # Flomo笔记数据
    with open(file_path) as file:
        soup = BeautifulSoup(file, 'html.parser')
        book_title = soup.select('.bookTitle')[0].string
        # 截取书名
        desc_index = book_title.find('（')
        if desc_index == -1:
            book_title = book_title[1:]
        else:
            book_title = book_title[1:desc_index]
        # 取标注和笔记
        div_arr = soup.select('div')
        for div in div_arr:
            if div['class'][0] == 'noteHeading' or div['class'][0] == 'noteText':
                div_content = div.contents[0].string.strip()
                result_arr.append(div_content)
        # 标注+笔记 -> flomo content
        for index, line in enumerate(result_arr):
            if line[:3] == '标注(':
                result_json.append('#kindle/' + book_title.strip() + '\n' + result_arr[index+1])
            if line[:5] == '笔记 - ':
                result_json.append(result_json.pop() + '\n' + delimiter + '\n笔记：' + result_arr[index+1])
        return result_json


def postDataToFlomo(json_data):
    for content in json_data:
        s = json.dumps({'content': content})
        headers = {
            'Content-Type': 'application/json; charset=UTF-8'
        }
        r = requests.post(api, data=s, headers=headers)
        print(type(r))
        break


post_data = open_html_file(html_file_path)
postDataToFlomo(post_data)
