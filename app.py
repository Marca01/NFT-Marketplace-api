import base64
import urllib.error

from flask import Flask, request, jsonify, send_file
import cv2     # Thư viện OpenCV
import numpy as np   # Thư viện numy để làm việc dữ liệu kiểu mảng
from PIL import Image
import json
from base64 import b64encode
import io as iioo
import os
from flask_cors import CORS
from imagekitio import ImageKit
from skimage import io
import sys
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
CORS(app)
# app.config['ENV'] = 'development'
# app.config['DEBUG'] = True
# app.config['TESTING'] = True
IMAGEKITIO_PRIVATE_KEY=os.getenv('IMAGEKITIO_PRIVATE_KEY')
imagekit = ImageKit(
    private_key=IMAGEKITIO_PRIVATE_KEY,
    public_key='public_f21ELrSgPPxirhamYY9KkzIGi1Q=',
    url_endpoint='https://ik.imagekit.io/Khale'
)

@app.route('/')
def home():
    return 'hello from NFT-Marketplace'

@app.route('/about')
def about():
    return 'about NFT-Marketplace'

@app.route('/edit/reset', methods=['POST'])
def resetImg():
    imageFile = request.files.get('image')
    imagekit.upload_file(
        file=imageFile,  # required
        file_name=f"{imageFile.filename}",  # required
        options={
            "use_unique_file_name": False,
        }
    )

    reset_url = imagekit.url({
        "path": f"/{imageFile.filename}",
        "url_endpoint": "https://ik.imagekit.io/Khale/"
    })

    return json.dumps({'msg': 'success', 'image': reset_url}, ensure_ascii=False)

@app.route('/edit/sharpen', methods=['POST'])
def sharpenImg():
    imageFile = request.files.get('image')
    # print(f'imageFile: {imageFile}')
    # image = Image.open(imageFile)
    # print(f'filename: {imageFile.filename}')
    # imageFile.save(os.path.join('images', imageFile.filename))
    # image = Image.open(imageFile)

    image = io.imread(imageFile)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # SHARPEN IMAGE
    kernel_sharpening = np.array([
        [-1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1],
        [-1, -1, 25, -1, -1],
        [-1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1],
    ])

    sharpened = cv2.filter2D(image, -1, kernel_sharpening)

    cv2.imwrite('images/transformed.jpg', sharpened)

    # sharpened_bytes_img = cv2.imencode('.jpg', sharpened)[1].tostring()

    # sharpened_img = bin(int.from_bytes(sharpened_bytes_img, byteorder=sys.byteorder))

    # encode base64 image
    img_to_base64 = Image.open(os.path.join('images', 'transformed.jpg'))
    byte_image = iioo.BytesIO()
    img_to_base64.save(byte_image, format='PNG')
    byte_image_value = byte_image.getvalue()
    base64_image = str(b64encode(byte_image_value).decode('utf-8'))

    imagekit.upload_file(
        file=base64_image,  # required
        file_name=f"{imageFile.filename}",  # required
        options={
            "folder": "/Sharpened_images/",
            "use_unique_file_name": False,
        }
    )

    sharpened_url = imagekit.url({
        "path": f"/Sharpened_images/{imageFile.filename}",
        "url_endpoint": "https://ik.imagekit.io/Khale/"
    })

    # filename = 'assets/test.jpg'
    # cv2.imwrite(filename, sharpened)
    # path = request.url_root+"assets/test.jpg"
    # return send_file(image, mimetype='image/jpg', as_attachment=True, attachment_filename=path)

    return json.dumps({'msg': 'success', 'image': sharpened_url}, ensure_ascii=False)
    # return 'ok'

@app.route('/edit/gaussianblur', methods=['POST'])
def gaussianBlurImg():
    imageFile = request.files.get('image')
    image = io.imread(imageFile)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # GAUSSIAN BLUR
    kernel_gaussian_blur = np.array([[-1, -1, -1],
                                     [-1, 9, -1],
                                     [-1, -1, -1]])
    smoothed = cv2.GaussianBlur(image, (247, 9), cv2.BORDER_DEFAULT)

    cv2.imwrite('images/transformed.jpg', smoothed)

    # encode base64 image
    img_to_base64 = Image.open(os.path.join('images', 'transformed.jpg'))
    byte_image = iioo.BytesIO()
    img_to_base64.save(byte_image, format='PNG')
    byte_image_value = byte_image.getvalue()
    base64_image = str(b64encode(byte_image_value).decode('utf-8'))

    imagekit.upload_file(
        file=base64_image,  # required
        file_name=f"{imageFile.filename}",  # required
        options={
            "folder": "/Blurred_images/",
            "use_unique_file_name": False,
        }
    )

    blurred_url = imagekit.url({
        "path": f"/Blurred_images/{imageFile.filename}",
        "url_endpoint": "https://ik.imagekit.io/Khale/"
    })

    return json.dumps({'msg': 'success', 'image': blurred_url}, ensure_ascii=False)

@app.route('/edit/negative', methods=['POST'])
def negativeImg():
    imageFile = request.files.get('image')
    image = io.imread(imageFile)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    negative = ~image

    cv2.imwrite('images/transformed.jpg', negative)

    # encode base64 image
    img_to_base64 = Image.open(os.path.join('images', 'transformed.jpg'))
    byte_image = iioo.BytesIO()
    img_to_base64.save(byte_image, format='PNG')
    byte_image_value = byte_image.getvalue()
    base64_image = str(b64encode(byte_image_value).decode('utf-8'))

    imagekit.upload_file(
        file=base64_image,  # required
        file_name=f"{imageFile.filename}",  # required
        options={
            "folder": "/Negative_images/",
            "use_unique_file_name": False,
        }
    )

    negative_url = imagekit.url({
        "path": f"/Negative_images/{imageFile.filename}",
        "url_endpoint": "https://ik.imagekit.io/Khale/"
    })

    return json.dumps({'msg': 'success', 'image': negative_url}, ensure_ascii=False)

if __name__ == '__main__':
    app.run(debug=True)


