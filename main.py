import os
import json
from flask import Flask, render_template, redirect, url_for, request, flash

IMAGE_DIR = './static/images'
JSON_FILE = './test.json'

# 指定されたディレクトリに存在する画像ファイル名をリスト化してソート
sorted_image_names = sorted([name for name in os.listdir(IMAGE_DIR) if '.jpg' in name or '.jpeg' in name])
id2img = {}
img2id = {}
# 各画像にidを振って, id->img, img->idのdictを作成
for i in range(0, len(sorted_image_names)):
    id2img[i] = sorted_image_names[i]
    img2id[sorted_image_names[i]] = i

with open(JSON_FILE) as fr:
    annotations = json.load(fr)

app = Flask(__name__)

@app.route('/')
def index():
    imgs = []
    for img_id, img in sorted(id2img.items()):
        label = get_label(img_id)
        imgs.append((img_id, img, label))

    return render_template('index.html', imgs=imgs)


@app.route('/annotate/<img_id>', methods=['POST', 'GET'])
def annotate(img_id=None):
    if not is_valid_id(img_id):
        flash('Image id is invalid...', 'error')
        return redirect(url_for('index'))
    
    img_id = int(img_id)
    img = id2img[img_id]
    
    if request.method == 'POST':
        ant = request.form['locked']
        if ant == 'locked':
            annotations[img] = 'locked'
        elif ant == 'non-locked':
            annotations[img] = 'non-locked'
        else:
            return redirect('/annotate/%d' % img_id)
        with open(JSON_FILE, 'w') as fw:
            json.dump(annotations, fw)
        flash('Annotation to %s is completed!' % img, 'success')
        # return render_template('annotate.html', id=img_id, img=img, label=annotations[img])

    return render_template('annotate.html', id=img_id, img=img, label=get_label(img_id))


def is_valid_id(img_id):
    if img_id is None or int(img_id) not in id2img:
        return False
    return True

# img_id: int
def get_label(img_id):
    img = id2img[img_id]
    if img in annotations:
        return annotations[img]
    else:
        return None


if __name__ == "__main__":
    app.secret_key = 'key'
    app.run(debug=True)
    
