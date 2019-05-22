import socket
import cv2

import awss3
import boto


aws_dl_object = awss3.AWSDownload()
aws_bucket = aws_dl_object.get_bucket()


def upload_file(file):
    print('start upload ')
    # file = '/Users/alinacodzy/Downloads/big_1576456.jpg'

    with open(file, 'rb') as h:
        pik = h.read()
    input_key = boto.s3.key.Key(aws_bucket)
    input_key.name = '/imgs/' + file.split('/')[-1]
    input_key.set_contents_from_string(pik)
    print(file)
    return input_key.name


def main():
    client()


def client():
    host = "18.222.114.115"  # get local machine name
    port = 8080  # Make sure it's within the > 1024 $$ <65535 range

    s = socket.socket()
    s.connect((host, port))
    print("connected")


    # photo = '/Users/alinacodzy/Downloads/opencv_pic.jpg'

    inp = input('->')

    while inp != 'q':
        # camera = cv2.VideoCapture(0)
        # return_value, image = camera.read()
        # photo = f'./opencv_{inp}.jpg'
        photo = f'opencv_{inp}.jpg'
        #
        # (h, w) = image.shape[:2]
        #
        # # calculate the center of the image
        # center = (w / 2, h / 2)
        # angle180 = 0
        # M = cv2.getRotationMatrix2D(center, angle180, 1.0)
        # rotated180 = cv2.warpAffine(image, M, (w, h))
        #
        # cv2.imwrite(photo, rotated180)
        # message = upload_file(photo)
        message = photo

        s.send(message.encode('utf-8'))
        data = s.recv(1024).decode('utf-8')
        print('Received from server: ' + data)
        inp = input('-> ')
    s.close()


if __name__ == '__main__':
    main()



