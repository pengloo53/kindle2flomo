from flask import Flask, request, redirect, url_for, jsonify
from flask_cors import CORS
import os
import json
import time
from parser import parse_csv_file, parse_html_file
from poster import post_all_to_flomo, format_data_to_json

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['csv', 'html'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app)


# 允许上传的格式
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# 解析笔记文件
@app.route('/parse', methods=['POST'])
def index():
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


# 批量导入flomo
@app.route('/post', methods=['POST'])
def post():
    if request.method == 'POST':
        print(request.form)
        api = request.form.get('api')
        delimiter = request.form.get('delimiter')
        data = request.form.get('data') or []
        data_list = json.loads(data)
        # flomo api 有 100 条每天的限制
        if len(data_list) > 100:
            return {
                "code": 1,
                "message": "Limit on the number of requests per day"
            }
        data_json = format_data_to_json(data_list, delimiter)
        is_order = request.form.get('is_order') or 'false'
        if is_order == 'false':
            is_order = False
        else:
            is_order = True
        if api and len(data):
            return post_all_to_flomo(data_json, api, is_order)


if __name__ == '__main__':
    app.run()
