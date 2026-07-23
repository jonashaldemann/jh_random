import glob
import os
from PIL import Image

ordner = "/Users/jonashaldemann/Downloads"

bilder = sorted(glob.glob(os.path.join(ordner, "*.jpg")))
bilder += sorted(glob.glob(os.path.join(ordner, "*.png")))

frames = []
for pfad in bilder:
    img = Image.open(pfad).convert("RGB")
    frames.append(img)

output_path = os.path.join(ordner, "gif.gif")

frames[0].save(
    output_path,
    save_all=True,
    append_images=frames[1:],
    duration=1000,
    loop=1
)