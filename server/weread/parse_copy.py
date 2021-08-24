# 解析微信读书笔记

def parse_weixin_notes(data):
    data_arr = data.split('\n')
    # 基础校验：少于 5 行，报错
    if len(data_arr) < 5:
        return {
            "result": []
        }
    # 测试微信读书笔记，结论：微信读书笔记存在重复项
    # test_arr = []
    # for line in data_arr:
    #     if line and line.startswith('>>'):
    #         test_arr.append(line)
    # print(len(test_arr))
    # print(test_arr)
    result_json = []    # 解析后的笔记数据，对象数组
    # 截取书名
    title = data_arr[0]
    # 取作者
    author = data_arr[1]
    # 取位置、标注和笔记
    place = ''
    note = ''
    for index, line in enumerate(data_arr):
        if line and index > 2:
            if line.startswith('◆'):
                place = line[2:]
            if line.startswith('>>'):
                highlight = line[3:]
                if data_arr[index-1]:
                    note = data_arr[index-1]
                result_json.append({
                    "place": place,
                    "highlight": highlight,
                    "note": note
                })
            note = ''
    return {
        "book_title": title,
        "book_author": author,
        "result": result_json
    }