from io import BytesIO
from flask import Flask, send_file, request, make_response
from PIL import Image
from re import match

app = Flask(__name__)


def hex_to_rgb(hex_val: str):
    assert match(r'[0-9a-fA-F]+', hex_val), f"Invalid hex code: {hex_val}"

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
    assert width.isnumeric(), f"Invalid width value: {width}"
    assert height.isnumeric(), f"Invalid height value: {height}"

    color_val = hex_to_rgb(color_hex)
    return Image.new('RGB', (int(width), int(height)), color=color_val)


def send_image(pillow_image):
    bytes_io = BytesIO()
    pillow_image.save(bytes_io, 'JPEG', quality=100)
    bytes_io.seek(0)
    return send_file(bytes_io, mimetype='image/jpeg')


@app.route('/')
def solid_image():
    for arg in ('width', 'height', 'hex-color'):
        if arg not in request.args:
            return make_response(f"{arg} not provided", 400)

    try:
        width = request.args.get('width')
        height = request.args.get('height')
        hex_color = request.args.get('hex-color')
        image = make_image(width, height, hex_color)
        return send_image(image)
    except Exception as e:
        return make_response(f"Error: {str(e)}", 500)


if __name__ == '__main__':
    app.run()
