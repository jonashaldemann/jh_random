import math
import requests
from PIL import Image

def latlon_to_tile(lat, lon, zoom):
    lat_rad = math.radians(lat)
    n = 2.0 ** zoom
    x = int((lon + 180.0) / 360.0 * n)
    y = int((1.0 - math.log(math.tan(lat_rad) + 1 / math.cos(lat_rad)) / math.pi) / 2.0 * n)
    return x, y


API_KEY = "DEIN_API_KEY"
SESSION = "DEINE_SESSION"  # vorher generieren!

def download_tile(z, x, y):
    url = f"https://tile.googleapis.com/v1/2dtiles/{z}/{x}/{y}?session={SESSION}&key={API_KEY}"
    response = requests.get(url)
    response.raise_for_status()
    return Image.open(BytesIO(response.content))

from io import BytesIO

def stitch_area(lat_min, lon_min, lat_max, lon_max, zoom):
    x_min, y_max = latlon_to_tile(lat_min, lon_min, zoom)
    x_max, y_min = latlon_to_tile(lat_max, lon_max, zoom)

    width = (x_max - x_min + 1) * 256
    height = (y_max - y_min + 1) * 256

    result = Image.new("RGB", (width, height))

    for x in range(x_min, x_max + 1):
        for y in range(y_min, y_max + 1):
            tile = download_tile(zoom, x, y)
            px = (x - x_min) * 256
            py = (y - y_min) * 256
            result.paste(tile, (px, py))

    return result


img = stitch_area(
    lat_min=47.36,
    lon_min=8.53,
    lat_max=47.38,
    lon_max=8.56,
    zoom=18
)

img.save("output.png")