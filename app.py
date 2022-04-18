import base64

from flask import Flask, request, jsonify, send_file
import cv2     # Thư viện OpenCV
import numpy as np   # Thư viện numy để làm việc dữ liệu kiểu mảng
from PIL import Image
import json
from base64 import b64encode
import io

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
    image = Image.open(imageFile)

    # base64 image
    byte_image = io.BytesIO()
    image.save(byte_image, format='PNG')
    byte_image_value = byte_image.getvalue()
    base64_image = b64encode(byte_image_value)
    # with open('base64Img.txt', 'w') as file:
    #     file.write(str(base64_image.decode('utf-8')))
    # return json.dumps({'msg': 'success', 'image': str(base64_image.decode('utf-8'))}, ensure_ascii=False)


    image = base64.b64decode(base64_image)
    npimg = np.fromstring(image, dtype=np.uint8)
    image = cv2.imdecode(npimg, 1)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # plt.figure(figsize=(20, 20))
    # plt.subplot(1, 2, 1)
    # plt.title("Original")
    # plt.imshow(image)
    kernel_sharpening = np.array([
        [-1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1],
        [-1, -1, 25, -1, -1],
        [-1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1],
    ])
    sharpened = cv2.filter2D(image, -1, kernel_sharpening)
    return send_file(sharpened, mimetype='image/png')
    # plt.subplot(1, 2, 2)
    # plt.title("Image Sharpening")
    # plt.imshow(sharpened)
    # plt.show()

if __name__ == '__main__':
    app.run(debug=True)


