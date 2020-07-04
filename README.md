# Solid Color API

This project is a simple Flask API to generate solid color images based on given parameters

## Project environemnt and setup
This project is built on top a Pipenv virtual environment, based on a Python 3.6.0 interpreter. The environment can be setup using the following commands:

``` shell script
pip install pipenv #in case you already have pipenv installed, this line can be skipped
pipenv shell
```

This project uses [Flask](https://flask.palletsprojects.com/en/1.1.x/) and [Python Imaging Library (PIL)](http://www.pythonware.com/products/pil/) as it's dependencies, asside from `BytesIO` and `re` from Python's standard library.

## Running the project
This project can be run as a simple Python script, as follows:
```shell script
python app.py
```

## Calling the API
The API accepts GET requests, requiring three parameters decribing the image to be generated:
+ the image's width, as `width`
+ the image's height, as `height`
+ an hexadecimal code of either length 3 or 6 corresponding to the desired color, as `hex-color`

If any of those parameters is not provided, the API will return a `400` error with a message indicating the missing parameter
```shell script
curl --location --request GET 'http://127.0.0.1:5000/?width=400hex-color=5F4B8B'
```
> Height not provided

Otherwise, the script will return a solid color JPEG image corresponding to the given parameters
 ```shell script
curl --location --request GET 'http://127.0.0.1:5000/?width=150&height=200&hex-color=888'
```
> ![Sample Image](./solid_color_sample_image.jpg)
