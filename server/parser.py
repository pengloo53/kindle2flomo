# 作者：鲁鹏
# Kindle 笔记文件解析，支持 csv 和 html 文件
# 解析内容：标注，笔记，标题

from bs4 import BeautifulSoup


# 去除字符串中的空格
def strip_space(string):
    new_string = ''
    for word in string:
        if word != ' ':
            new_string = new_string + word
    return new_string


def parse_csv_file(file_path):
    result_json = []    # 解析后的笔记数据，对象数组
    with open(file_path, encoding='utf8') as file:
        for index, line in enumerate(file):
            # 截取书名
            if index == 1:
                desc_index = line.find('（')
                if desc_index == -1:
                    title = line[1:]
                else:
                    title = line[1: desc_index]
            # 取标注和笔记
            if line[1:3] == '标注':
                highlight = line.split(',')[3][1:-2]
                tags = '#kindle/' + title
                result_json.append({
                    "tags": tags,
                    "highlight": highlight
                })
            if line[1:3] == '笔记':
                note = line.split(',')[3][1:-2]
                the_result = result_json.pop()
                the_result['note'] = note
                result_json.append(the_result)
        return result_json


def parse_html_file(file_path):
    result_arr = []     # HTML中有效数据
    result_json = []    # 解析后的笔记数据，对象数组
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
                tags = '#kindle/' + book_title.strip()
                result_json.append({
                    "tags": tags,
                    "highlight": highlight
                })
            if line[:5] == '笔记 - ' or line[:5] == '备注 - ':
                note = result_arr[index+1]
                the_result = result_json.pop()
                the_result['note'] = note
                result_json.append(the_result)
        return result_json
