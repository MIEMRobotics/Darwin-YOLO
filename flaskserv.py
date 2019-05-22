from flask import Flask
from flask import request
app = Flask(__name__)
import os

@app.route('/', methods=['POST'])
def read_data():
    if request.method == 'POST':
        print('Got connection from')
        data = request.data
        name = '/mys3bucket/post_imj.jpg'
        with open(name, 'rb') as f:
            f.write(data)

        os.system(
            f"cd /mys3bucket/robots/darknet-master && ./darknet detect cfg/yolov3.cfg yolov3.weights {name} >/mys3bucket/robots/res.txt")

        data = open('/mys3bucket/robots/res.txt', 'rb').read()
        print('answer sent')

    return data


if __name__ == '__main__':
    app.run(debug=True, host='', port='5006')
