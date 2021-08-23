# 解析微信读书笔记

def parse_weixin_notes(data):
    data_arr = data.split('\n')
    print(data_arr)
    result_json = []    # 解析后的笔记数据，对象数组
    # 截取书名
    title = data_arr[0]
    # 取作者
    author = data_arr[1]
    # 取位置、标注和笔记
    for index, line in enumerate(data_arr):
        if line[:1] == '◆':
            place = line[2:]
            result_json.append({
                "place": place
            })
        # if n
        return {
            "book_title": title,
            "book_author": author,
            "result": result_json
        }