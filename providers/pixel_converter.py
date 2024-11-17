import json

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

class PixelConverter:
    def imageToPixel(self, image, pixel_offset, brightness=128):
        pixels = image.load()
        width, height = image.size
        pixel_data = []

        for y in range(height):
            for x in range(width):
                r, g, b = pixels[x, y]
                hex_color = '{:02x}{:02x}{:02x}'.format(r, g, b)
                if len(pixel_data) == 0 or pixel_data[-2] != hex_color:
                    pixel_data.append(x + y * width)
                    pixel_data.append(hex_color)
                elif isinstance(pixel_data[-1], str):
                    pixel_data.insert(-1, x + y * width)

        json_format = {"on": True, "bri": brightness, "seg": {"id": pixel_offset, "i": pixel_data}}
        return json_format