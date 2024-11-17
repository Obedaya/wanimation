import datetime
import time
from typing import Any

import requests

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from .text_provider import TextProvider


LONGITUDE = 0
LATITUDE = 0

class AnimationProvider(TextProvider):
    def __init__(self, matrix, fps=30) -> None:
        super().__init__(matrix, fps)
        self.font = ImageFont.truetype("fonts/Berkelium1541.ttf", size=6)
        self.textColor = (150, 150, 20)
        self.titleColor = (100, 200, 200)
        self.weather = WeatherAPI(LATITUDE, LONGITUDE)

    def displayContent(self, t) -> None:
        image = self.createImageFor()
        self.matrix.displayImage(image)
        time.sleep(t)

    def createImageFor(self) -> Image:
        image = Image.new('RGB', self.matrix.getSize(), (0, 0, 0))

        draw = ImageDraw.Draw(image)

        current_weather = self.weather.getCurrentWeather()
        print(current_weather)

        temperature = current_weather["temperature_2m"]
        (r, g, b) = self.weather.temperature_to_color(temperature)

        # Choose icon 8x8 based on weather code
        if current_weather["is_day"]:
            icon = Image.open(f"weather_icons/day/{current_weather['weather_code']}.png")
        else:
            icon = Image.open(f"weather_icons/night/{current_weather['weather_code']}.png")
        image.paste(icon, (0, 0))

        # Draw temperature behind icon
        draw.text((9, 1), f"{temperature}°C", (r, g, b), font=self.font)


        return image


class WeatherAPI:
    def __init__(self, latitude: float, longitude: float) -> None:
        self.latitude = latitude
        self.longitude = longitude
        self.url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,is_day,weather_code&daily=weather_code,temperature_2m_max,temperature_2m_min&timezone=Europe%2FBerlin&forecast_days=3"
        self.weather = None
        self.lastUpdate = None
        self._getWeather()

    def _getWeather(self) -> None:
        # Only update weather every 1h
        if self.lastUpdate is None or (datetime.datetime.now() - self.lastUpdate).seconds > 3600:
            response = requests.get(self.url)
            self.weather = response.json()
            self.lastUpdate = datetime.datetime.now()
            print("Updated weather")

    def getCurrentWeather(self) -> dict[str, Any]:
        self._getWeather()
        return self.weather['current']

    def getWeatherForecast(self) -> dict[str, Any]:
        self._getWeather()
        return self.weather['daily']

    def temperature_to_color(self, temperature):
        # Ensure temperature stays within bounds
        clamped_temp = max(-20, min(temperature, 40))

        # Calculate ratio for interpolation
        if clamped_temp <= 0:
            # Blue to White
            ratio = (clamped_temp + 20) / 20
            r, g, b = (255 * ratio, 255 * ratio, 255)
        else:
            # White to Red
            ratio = clamped_temp / 40
            r, g, b = (255, 255 * (1 - ratio), 255 * (1 - ratio))

        return (int(r), int(g), int(b))