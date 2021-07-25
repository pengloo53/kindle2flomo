from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
import time
from kindle.parser import parse_csv_file, parse_html_file
from poster import post_to_flomo, format_data_to_content

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['csv', 'html'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app)


# 允许上传的格式
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# 解析笔记文件服务
@app.route('/parse', methods=['POST'])
def parse():
    result = []
    if request.method == 'POST':
        print(request.files)
        file = request.files.get('file')
        if file and allowed_file(file.filename):
            filename = file.filename.rsplit('.', 1)[0]
            ext = file.filename.rsplit('.', 1)[1]
            new_filename = filename + '_' + str(time.time()) + '.' + ext
            file_save_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
            file.save(file_save_path)
            if ext == 'html':
                result = parse_html_file(file_save_path)
            elif ext == 'csv':
                result = parse_csv_file(file_save_path)
    return jsonify(result)


# 导入 MEMO (单条)
@app.route('/post', methods=['POST'])
def post():
    if request.method == 'POST':
        api = request.form.get('api')
        tag = request.form.get('tag') or ''
        delimiter = request.form.get('delimiter') or ''
        highlight = request.form.get('highlight') or ''
        note = request.form.get('note') or ''
        order = request.form.get('order')
        content = format_data_to_content({
            'tag': tag,
            'delimiter': delimiter,
            'note': note,
            'highlight': highlight
        }, order)
        if api:
            return post_to_flomo(content, api)
        else:
            return 'No api'


if __name__ == '__main__':
    app.run()
