import base64

from flask import Flask, request, jsonify, send_file
import cv2     # Thư viện OpenCV
import numpy as np   # Thư viện numy để làm việc dữ liệu kiểu mảng
from PIL import Image
import json
from base64 import b64encode
import io
import os

app = Flask(__name__)
# app.config['ENV'] = 'development'
# app.config['DEBUG'] = True
# app.config['TESTING'] = True

@app.route('/')
def home():
    return 'hello from NFT-Marketplace'

@app.route('/about')
def about():
    return 'about NFT-Marketplace'

@app.route('/edit/sharpen', methods=['POST'])
def sharpenImg():
    imageFile = request.files.get('image')
    imageFile.save(os.path.join('images', imageFile.filename))
    # image = Image.open(imageFile)

    image = cv2.imread(os.path.join('images', imageFile.filename))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # SHARPEN IMAGE
    kernel_sharpening = np.array([
        [-1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1],
        [-1, -1, 25, -1, -1],
        [-1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1],
    ])

    # GAUSSIAN BLUR
    kernel_gaussian_blur = np.array([[-1, -1, -1],
                                  [-1, 9, -1],
                                  [-1, -1, -1]])
    # smoothed = cv2.GaussianBlur(image, (247, 9), cv2.BORDER_DEFAULT)

    sharpened = cv2.filter2D(image, -1, kernel_sharpening)

    filename = 'assets/test.jpg'
    cv2.imwrite(filename, sharpened)
    path = request.url_root+"assets/test.jpg"

    image = cv2.imread(filename)
    # return send_file(image, mimetype='image/jpg', as_attachment=True, attachment_filename=path)
    base64_image = str(b64encode(image).decode('utf-8'))
    return json.dumps({'msg': 'success', 'image': base64_image}, ensure_ascii=False)

@app.route('/edit/gaussianblur', methods=['POST'])
def gaussianBlurImg():
    imageFile = request.files.get('image')
    imageFile.save(os.path.join('images', imageFile.filename))

    image = cv2.imread(os.path.join('images', imageFile.filename))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # GAUSSIAN BLUR
    kernel_gaussian_blur = np.array([[-1, -1, -1],
                                     [-1, 9, -1],
                                     [-1, -1, -1]])
    smoothed = cv2.GaussianBlur(image, (247, 9), cv2.BORDER_DEFAULT)

    filename = 'assets/test.jpg'
    cv2.imwrite(filename, smoothed)
    path = request.url_root + "assets/test.jpg"

    image = cv2.imread(filename)
    base64_image = str(b64encode(image).decode('utf-8'))
    return json.dumps({'msg': 'success', 'image': base64_image}, ensure_ascii=False)

if __name__ == '__main__':
    app.run(debug=True)


