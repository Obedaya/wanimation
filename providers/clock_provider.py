from dis import show_code
import time
import datetime
import numpy as np
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
from .text_provider import TextProvider

from  providers.utils import color_hex2triplet, color_mult



class ClockProvider(TextProvider):
    def __init__(self, matrix, fps=5) -> None:
        super().__init__(matrix, fps)
        self.font = ImageFont.truetype("fonts/digital-7.ttf", size=30)
        self.textColor = (150,150,20)
        self.titleColor = (100,200,200)

    def displayContent(self, t) -> None:
        starttime = time.time()
        while time.time() < (starttime + float(t)):
            image = self.createImageFor()
            self.matrix.displayImage(image)
            time.sleep(1/self.fps)


    def createImageFor(self) -> Image:
        image = Image.new('RGB', self.matrix.getSize(), (0,0,0))
        draw = ImageDraw.Draw(image)
        (x,y) = self.matrix.getCenter()
        y = y - round(self.font.size/2)
        super().centeredtext(draw, (x,y), time.strftime("%H:%M:%S"))
        return image