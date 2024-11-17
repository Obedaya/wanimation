#!/usr/bin/env python3

import socket
import time
import requests
import json
from PIL import Image
from .pixel_converter import PixelConverter

WLED_IP = "10.1.0.67"

# on macOS: sudo sysctl -w net.inet.udp.maxdgram=65535
# net.inet.udp.maxdgram: 9216 -> 65535

class Matrix:
    def __init__(self, size):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
        self.t = None
        self.size = size
        self.pixelConverter = PixelConverter()
    
    def displayImage(self, im):
        # im = Image.open("./album.jpg")
        #im = im.transpose(Image.FLIP_LEFT_RIGHT)
        #im = im.transpose(Image.FLIP_TOP_BOTTOM)
        im.thumbnail(self.size, Image.ANTIALIAS)

        background = Image.new('RGB', self.size, (0, 0, 0))
        background.paste(im, (int((self.size[0] - im.size[0]) / 2), int((self.size[1] - im.size[1]) / 2)))

        self.sendImage(background)

    def sendImage(self, im):
        json_image = self.pixelConverter.imageToPixel(im, 0)

        # Send JSON to WLED
        url = f"http://{WLED_IP}/json/state"
        headers = {'Content-Type': 'application/json'}

        response = requests.post(url, headers=headers, data=json.dumps(json_image))

    def getWidth(self):
        return self.size[0]

    def getHight(self):
        return self.size[1]
    
    def getSize(self):
        return self.size

    def getCenter(self):
        return (round(self.size[0]/2),round(self.size[1]/2))