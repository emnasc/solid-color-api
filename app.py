from io import BytesIO
from flask import Flask, send_file, request, make_response
from PIL import Image
from re import findall

app = Flask(__name__)


def hex_to_rgb(hex_val: str):
    assert findall(r'[0-9a-fA-F]+', hex_val), "Invalid hex code"

    if len(hex_val) not in (3, 6):
        raise Exception("Invalid hex code length")
    elif len(hex_val) == 3:
        r_hex, g_hex, b_hex = hex_val[0] * 2, \
                              hex_val[1] * 2, \
                              hex_val[2] * 2
    elif len(hex_val) == 6:
        r_hex, g_hex, b_hex = hex_val[0:2],\
                              hex_val[2:4],\
                              hex_val[4:6]

    return int(r_hex, 16), int(g_hex, 16), int(b_hex, 16)


def make_image(width, height, color_hex):
    assert width.isnumeric(), "Invalid width value"
    assert height.isnumeric(), "Invalid height value"

    color_val = hex_to_rgb(color_hex)
    return Image.new('RGB', (int(width), int(height)), color=color_val)


def send_image(pillow_image):
    bytes_io = BytesIO()
    pillow_image.save(bytes_io, 'JPEG', quality=100)
    bytes_io.seek(0)
    return send_file(bytes_io, mimetype='image/jpeg')


@app.route('/')
def solid_image():
    if 'width' not in request.args:
        return make_response("width not provided", 400)
    elif 'height' not in request.args:
        return make_response("height not provided", 400)
    elif 'hex-color' not in request.args:
        return make_response("hex-color not provided", 400)

    width = request.args.get('width')
    height = request.args.get('height')
    hex_color = request.args.get('hex-color')
    image = make_image(width, height, hex_color)
    return send_image(image)


if __name__ == '__main__':
    app.run()
