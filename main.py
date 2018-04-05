# -*- coding: utf-8 -*-


import os
import json
from flask import Flask, render_template, redirect, url_for, request

IMAGE_DIR = './images'
JSON_FILE = './test.json'


sorted_image_names = sorted(os.listdir(IMAGE_DIR))
id2img = {}
img2id = {}
for i in range(0, len(sorted_image_names)):
    id2img[i] = sorted_image_names[i]
    img2id[sorted_image_names[i]] = i

with open(JSON_FILE) as fr:
    annotations = json.load(fr)

app = Flask(__name__)

@app.route('/')
def index():
    imgs = []
    for id, img in sorted(id2img.items()):
        flag = get_flag(id)
        imgs.append((id, img, flag))

    return render_template('index.html', imgs=imgs)

@app.route('/annotate/<id>')
def annotate(id=None):
    # TODO: 不正な値が与えられたときは前の画面でエラーメッセージを出したい
    if not is_valid_id:
        flash('Invalid id.')
        return redirect('/')

    id=int(id)
    img = id2img[id]
    flag = get_flag(id)
    
    return render_template('annotate.html', id=id, img=img, flag=flag)

# TODO: POSTでアノテーションの結果を受け取り，annotationsの中身を書き換え，jsonファイルを更新する
@app.route('/save/<id>', methods=['POST'])
def save(id=None):
    if not is_valid_id: return redirect('/')
    
    id = int(id)
    img = id2img[id]
    if request.method == 'POST':
        ant = request.form['locked']
        if ant == 'locked':
            annotations[img] = 'locked'
        elif ant == 'non-locked':
            annotations[img] = 'non-locked'
        else:
            return redirect('/annotate/%d' % id)
        with open(JSON_FILE, 'w') as fw:
            json.dump(annotations, fw)
    
    return redirect('/')


def is_valid_id(id):
    if id is None or type(id) != int or int(id) not in id2img:
        return False
    return True


# id: int
def get_flag(id):
    img = id2img[id]
    if img in annotations:
        return annotations[img]
    else:
        return None



if __name__ == "__main__":
    app.run(debug=True)