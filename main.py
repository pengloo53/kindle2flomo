import json
import time
from bs4 import BeautifulSoup
import requests

# api
api = 'https://flomoapp.com/iwh/MzIzNQ/70306b07dbfe6d7be19a17c02e35592a/'
# 分隔符
delimiter = '>>>>>>>>>'
# 文件路径
html_file_path = 'files/不拘一格：网飞的自由与责任工作法.html'
csv_file_path = 'files/Kindle-Notebook.csv'
# 是否顺序查看
is_order = True


# 去除字符串中的空格
def strip_space(string):
    new_string = ''
    for word in string:
        if word != ' ':
            new_string = new_string + word
    return new_string


def parse_csv_file(file_path):
    result_json = []    # Flomo笔记数据
    with open(file_path, encoding='utf8') as file:
        for index, line in enumerate(file):
            # 截取书名
            if index == 1:
                desc_index = line.find('（')
                if desc_index == -1:
                    title = line[1:]
                else:
                    title = line[1: desc_index]
            # 获取作者
            if index == 2:
                author = line
            # 取标注和笔记
            if line[1:3] == '标注':
                highlight = line.split(',')[3][1:-2]
                result_json.append('#kindle/' + title + '\n' + highlight)
            if line[1:3] == '笔记':
                note = line.split(',')[3][1:-2]
                result_json.append(result_json.pop() + '\n' + delimiter + '\n笔记：' + note)
        return result_json


def parse_html_file(file_path):
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
                highlight = strip_space(result_arr[index+1])
                result_json.append('#kindle/' + book_title.strip() + '\n' + highlight)
            if line[:5] == '笔记 - ' or line[:5] == '备注 - ':
                result_json.append(result_json.pop() + '\n' + delimiter + '\n笔记：' + result_arr[index+1])
        return result_json


def post_data_to_flomo(json_data):
    # 顺序查看，那么需要倒序插入笔记
    if is_order:
        json_data.reverse()
    for index, content in enumerate(json_data):
        s = json.dumps({'content': content})
        headers = {
            'Content-Type': 'application/json; charset=UTF-8'
        }
        r = requests.post(api, data=s, headers=headers)
        print('post ' + str(index+1) + ' success.')
        time.sleep(1)


# post_data = parse_html_file(html_file_path)
post_data = parse_csv_file(csv_file_path)
post_data_to_flomo(post_data)