from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
import time
import hashlib
from kindle.parser import parse_csv_file, parse_html_file
from poster import post_to_flomo, format_data_to_content
from weread.parse_copy import parse_weixin_notes

BASE_PATH = os.path.dirname(__file__)
UPLOAD_FOLDER = './kindle/uploads'
ALLOWED_EXTENSIONS = set(['csv', 'html'])

app = Flask(__name__)
CORS(app)


# 允许上传的格式
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# 解析 Kindle 笔记文件，返回 result 对象
def parse_file(filename):
    result = {}
    ext = filename.rsplit('.', 1)[1]
    file_save_path = os.path.join(BASE_PATH, UPLOAD_FOLDER, filename)
    if ext == 'html':
        result = parse_html_file(file_save_path)
    elif ext == 'csv':
        result = parse_csv_file(file_save_path)
    else:
        return result


# 保存上传的文件，返回文件路径
def save_file(file):
    if file and allowed_file(file.filename):
        filename = file.filename
        ext = filename.rsplit('.', 1)[1]
        # 重命名文件保存，源文件名加上时间后缀，然后哈希散列，确保文件唯一性
        filename = hashlib.md5(bytes(filename + '_' + str(time.time()), encoding="utf-8")) + '.' + ext
        file_save_path = os.path.join(BASE_PATH, UPLOAD_FOLDER, filename)
        file.save(file_save_path)
        return file_save_path


# 获取读书笔记，根据笔记文件名
@app.route('/get/<filename>', methods=['GET'])
def get_notes(filename):
    return parse_file(filename)


# 解析笔记文件服务，POST 上传文件并解析
@app.route('/parse', methods=['POST'])
def parse():
    result = []
    file = request.files.get('file')
    file_path = save_file(file)
    
        
        
       
        result = parse_file(filename)
        return jsonify({
            'data': result,
            'filename': filename
        })
    else:
        return result


# 导入读书笔记到 flomo
@app.route('/post', methods=['POST'])
def post():
    api = request.form.get('api')
    tag = request.form.get('tag') or ''
    delimiter = request.form.get('delimiter') or ''
    highlight = request.form.get('highlight') or ''
    note_prefix = request.form.get('note_prefix') or ''
    highlight_prefix = request.form.get('highlight_prefix') or ''
    note = request.form.get('note') or ''
    order = request.form.get('order') or 'down'
    content = format_data_to_content({
        'tag': tag,
        'delimiter': delimiter,
        'note_prefix': note_prefix,
        'note': note,
        'highlight_prefix': highlight_prefix,
        'highlight': highlight
    }, order)
    if api:
        return post_to_flomo(content, api)
    else:
        return 'No api'


# 导入编辑的内容到 flomo
@app.route('/post_single', methods=['POST'])
def post_single():
    api = request.form.get('api')
    content = request.form.get('content')
    if api:
        return post_to_flomo(content, api)
    else: 
        return 'No api'


# 解析微信笔记
@app.route('/parse_weixin', methods=['POST'])
def parse_weixin():
    data = request.form.get('data')
    if data:
        return parse_weixin_notes(data)


if __name__ == '__main__':
    app.run()
