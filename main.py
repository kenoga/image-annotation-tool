import os
import json
import glob
from collections import defaultdict
from flask import Flask, render_template, redirect, url_for, request, flash

STATIC_DIRNAME = 'static'
IMAGE_DIR = './static/images'
JSON_FILE = './test.json'
LABELS = ["ok", "one-eye", "no-eye", "closed-eyes", "other"]

# 指定されたディレクトリに存在する画像ファイル名をリスト化してソート
# TODO: static内に存在すればどんなパスでも取得できるようにする
img_paths = sorted([path for path in glob.glob(os.path.join(IMAGE_DIR, "*/*/*.jpg"))])

with open(JSON_FILE) as fr:
    annotations = json.load(fr)

app = Flask(__name__)

@app.route('/')
def index():
    imgs = []
    for index, img_path in enumerate(img_paths):
        img_name = get_img_name(img_path)
        label = get_label(img_name)
        imgs.append((index, img_name, label))

    return render_template('index.html', imgs=imgs)


@app.route('/annotate/<img_index>', methods=['POST', 'GET'])
def annotate(img_index=None):
    if not is_valid_index(img_index):
        flash('Image id is invalid...', 'error')
        return redirect(url_for('index'))
    img_index = int(img_index)
    img_path = img_paths[img_index]
    img_name = get_img_name(img_path)
    img_path_for_client = get_img_path_for_client(img_path)
    
    if request.method == 'POST':
        ant = request.form['ant']
        annotations[img_name] = ant
        with open(JSON_FILE, 'w') as fw:
            json.dump(annotations, fw)
        flash('Annotation to %s is completed!' % img_name, 'success')

    label = get_label(img_name)
    return render_template('annotate.html', 
                           index=img_index,
                           img_name=img_name,
                           img_path=img_path_for_client,
                           label=label,
                           labels=LABELS,
                           checked_or_not=create_checked_or_not_list(label, LABELS))

def create_checked_or_not_list(label, labels):
    li = [""] * len(labels)
    if label is None:
        li[0] = "checked"
    else:
        li[label.index(label)] = "checked"
    return li

def is_valid_index(img_index):
    if img_index is None or int(img_index) < 0 or int(img_index) >= len(img_paths):
        return False
    return True

def get_label(img_name):
    if img_name in annotations:
        return annotations[img_name]
    else:
        return None

def get_img_name(img_path):
    return os.path.basename(img_path)
    
def get_img_path_for_client(img_path):
    return "/static" + img_path.split(STATIC_DIRNAME)[1]
    

if __name__ == "__main__":
    app.secret_key = 'key'
    app.run(debug=True)
    
