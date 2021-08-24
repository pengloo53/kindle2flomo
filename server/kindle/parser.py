# 作者：鲁鹏
# Kindle 笔记文件解析，支持 csv 和 html 文件
# 解析内容：标注，笔记，标题
import re
from bs4 import BeautifulSoup


# 去除字符串中的空格
def strip_space_old(string):
    new_string = ''
    for word in string:
        if word != ' ':
            new_string = new_string + word
    return new_string

# 去除字符串中的空格，兼容中英文
def strip_space(text):
    match_regex = re.compile(
        u'[\u4e00-\u9fa5。\.,，:：《》、\(\)（）]{1} +(?<![a-zA-Z])|\d+ +| +\d+|[a-z A-Z]+')
    should_replace_list = match_regex.findall(text)
    order_replace_list = sorted(
        should_replace_list, key=lambda i: len(i), reverse=True)
    for i in order_replace_list:
        if i == u' ':
            continue
        new_i = i.strip()
        text = text.replace(i, new_i)
    return text


# 判断是标注还是笔记
def highlight_or_note(str):
    if str.startswith('标注(') or str.startswith('标注 (') or str.startswith('Highlight(') or str.startswith('Highlight ('):
        return 'highlight'
    elif str.startswith('笔记 -') or str.startswith('备注 -') or str.startswith('Note -'):
        return 'note'


# 截取书名，去除书名的描述部分
def format_book_title(title):
    title = title.strip()
    if title.startswith('《'):
        title = title[1:]
    if title.endswith('》'):
        title = title[:-1]
    return re.split('[(（]', title)[0].strip()


def parse_csv_file(file_path):
    result_json = []    # 解析后的笔记数据，对象数组
    with open(file_path, encoding='utf8') as file:
        for index, line in enumerate(file):
            # 截取书名
            if index == 1:
                title = format_book_title(line[1:])
            # 取位置标注和笔记
            line_arr = line.split(',')
            line_begin_str = line_arr[0][1:-2]  # 去掉引号
            if highlight_or_note(line_begin_str) == 'highlight':
                place = line_arr[1][1:-2]
                highlight = line_arr[3][1:-2]
                result_json.append({
                    "place": place,
                    "highlight": highlight
                })
            if highlight_or_note(line_begin_str) == 'note':
                note = line.split(',')[3][1:-2]
                the_result = result_json.pop()
                the_result['note'] = note
                result_json.append(the_result)
        return {
            "book_title": title,
            "result": result_json
        }


def parse_html_file(file_path):
    result_arr = []     # HTML中有效数据
    result_json = []    # 解析后的笔记数据，对象数组
    with open(file_path, encoding='utf8') as file:
        soup = BeautifulSoup(file, 'html5lib')
        book_title = soup.select('.bookTitle')[0].string
        book_title = format_book_title(book_title)
        # 取标注和笔记
        # 由于 Mac 阅读软件导出的 HTML 文件结构有缺陷（缺少关闭标签）导致解析过程出现混乱，逻辑只能随之混乱。
        # 根据 Mac 导出的 HTML 不存在 div.noteHeading 的标签来区分
        div_noteHeading = soup.select('div.noteHeading')
        if len(div_noteHeading) == 0:
            for element in soup.body:
                if element.name:    # 删除空字符串节点
                    # 第一个 noteHeading 莫名在 bodyContainer 下
                    if element['class'][0] == 'bodyContainer':
                        if len(element.h3.contents) == 1:
                            result_arr.append(
                                element.h3.contents[0].string.strip())
                        else:
                            result_arr.append(element.h3.contents[0].string.strip(
                            ) + element.h3.contents[2].string.strip())
                    elif element['class'][0] == 'noteText':
                        result_arr.append(element.contents[0].string.strip())
                        if element.h3:
                            if len(element.h3.contents) == 1:
                                result_arr.append(
                                    element.h3.contents[0].string.strip())
                            else:
                                result_arr.append(element.h3.contents[0].string.strip(
                                ) + element.h3.contents[2].string.strip())
        # Windows 阅读软件 和 手机导出
        else:
            div_arr = soup.select('div')
            for div in div_arr:
                if div['class'][0] == 'noteHeading' or div['class'][0] == 'noteText':
                    if len(div.contents) == 1:
                        div_content = div.contents[0].string.strip()
                    else:
                        div_content = div.contents[0].string.strip(
                        ) + div.contents[2].string.strip()
                    result_arr.append(div_content)
        # print(result_arr)
        # 位置+标注+笔记
        for index, line in enumerate(result_arr):
            if highlight_or_note(line) == 'highlight':
                place = result_arr[index].split('-')[1].strip()
                highlight = strip_space(result_arr[index+1])
                result_json.append({
                    "place": place,
                    "highlight": highlight
                })
            if highlight_or_note(line) == 'note':
                note = result_arr[index+1]
                the_result = result_json.pop()
                the_result['note'] = note
                result_json.append(the_result)
        return {
            "book_title": book_title,
            "result": result_json
        }
