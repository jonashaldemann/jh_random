import os
import json
import requests
import laspy
import rasterio
from rasterio.merge import merge
import pdal
import glob
from pyproj import Transformer

# ---------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------
# Pfad zum Downloads-Ordner des aktuellen Users
downloads = os.path.expanduser("/Users/jonashaldemann/Downloads")

# Suche nach .laz und .las Dateien
laz_files = glob.glob(os.path.join(downloads, "*.laz"))
las_files = glob.glob(os.path.join(downloads, "*.las"))

pointcloud_files = laz_files + las_files

if not pointcloud_files:
    raise FileNotFoundError("Keine .las oder .laz Datei im Downloads-Ordner gefunden!")

# Nimm die erste gefundene Datei
valid_pointclouds = []

for pc in pointcloud_files:
    ext = os.path.splitext(pc)[1].lower()
    if ext in [".las", ".laz"]:
        valid_pointclouds.append(pc)

if not valid_pointclouds:
    raise FileNotFoundError("Keine gültigen LAS/LAZ Dateien gefunden!")

print("Gefundene Punktwolken:", valid_pointclouds)

WORKDIR = "swisstopo_data"
ORTHO_MERGED = os.path.join(WORKDIR, "swissimage_merged.tif")
OUTPUT_LAZ = os.path.join(downloads, "colored.laz")

STAC_API = "https://data.geo.admin.ch/api/stac/v0.9/collections/ch.swisstopo.swissimage-dop10/items"


# ---------------------------------------------------------------------
# CHECK CRS
# ---------------------------------------------------------------------

def check_crs(laz_path):
    las = laspy.read(laz_path)
    crs = las.header.parse_crs()
    
    if crs is None:
        print("Warnung: LAS hat kein CRS → setze EPSG:2056 in PDAL Pipeline")
    else:
        print("CRS gefunden:", crs)


# ---------------------------------------------------------------------
# STEP 1: Bounding Box from LAZ
# ---------------------------------------------------------------------
def get_laz_bbox(laz_path):
    las = laspy.read(laz_path)
    minx, maxx = float(las.x.min()), float(las.x.max())
    miny, maxy = float(las.y.min()), float(las.y.max())
    # Prüfen, ob BBox in Schweizer Datenbereich liegt
    if minx < 2420000 or maxx > 2830000 or miny < 1070000 or maxy > 1300000:
        raise RuntimeError(f"BBox liegt außerhalb des Swissimage Datenbereichs: {minx},{miny},{maxx},{maxy}")
    return [minx, miny, maxx, maxy]

# ---------------------------------------------------------------------
# STEP 2: Query STAC API
# ---------------------------------------------------------------------
def query_stac(bbox):
    bbox_str = ",".join(map(str, bbox))
    url = f"{STAC_API}?bbox={bbox_str}"
    response = requests.get(url)

    if not response.ok:
        raise RuntimeError(f"STAC API request failed: {response.status_code} {response.text}")

    data = response.json()

    if 'features' not in data or len(data['features']) == 0:
        raise RuntimeError(f"Keine Features von STAC API zurückgegeben. BBox: {bbox_str}")

    tiff_urls = []
    for feature in data['features']:
        assets = feature.get('assets', {})
        for key in assets:
            if key.endswith('_0.1_2056.tif'):
                tiff_urls.append(assets[key]['href'])

    if not tiff_urls:
        raise RuntimeError("Keine passenden TIFF URLs gefunden!")

    return tiff_urls

# ---------------------------------------------------------------------
# STEP 3: Download TIFFs
# ---------------------------------------------------------------------
def download_files(urls, folder):
    os.makedirs(folder, exist_ok=True)
    paths = []

    for url in urls:
        filename = os.path.join(folder, url.split('/')[-1])
        if not os.path.exists(filename):
            print(f"Downloading {filename}")
            r = requests.get(url)
            with open(filename, 'wb') as f:
                f.write(r.content)
        paths.append(filename)

    return paths

# ---------------------------------------------------------------------
# STEP 4: Merge TIFFs
# ---------------------------------------------------------------------
def merge_tiffs(tiff_paths, output_path):
    src_files = [rasterio.open(p) for p in tiff_paths]
    mosaic, out_trans = merge(src_files)

    out_meta = src_files[0].meta.copy()
    out_meta.update({
        'driver': 'GTiff',
        'height': mosaic.shape[1],
        'width': mosaic.shape[2],
        'transform': out_trans
    })

    with rasterio.open(output_path, 'w', **out_meta) as dest:
        dest.write(mosaic)

# ---------------------------------------------------------------------
# STEP 5: Colorize with PDAL
# ---------------------------------------------------------------------
def colorize_laz(input_laz, raster_tif, output_laz):
    os.environ['PROJ_NETWORK'] = 'OFF'  # Mac: verhindert Hängen beim Import
    pipeline = {
        'pipeline': [
            {
                "type": "readers.las",
                "filename": input_laz,
                "spatialreference": "EPSG:2056"
            },
            {
                "type": "filters.colorization",
                "raster": raster_tif
            },
            {
                "type": "writers.las",
                "filename": output_laz,
                "extra_dims": "all"
            }
        ]
    }

    p = pdal.Pipeline(json.dumps(pipeline))
    p.execute()

# ---------------------------------------------------------------------
# MAIN WORKFLOW
# ---------------------------------------------------------------------
if __name__ == '__main__':
    # BBox nur einmal von allen Dateien berechnen
    print("Reading bounding box...")
    all_bbox = [get_laz_bbox(pc) for pc in valid_pointclouds]

    # kombiniere Bounding Boxes zu einer großen Box
    minx = min(b[0] for b in all_bbox)
    miny = min(b[1] for b in all_bbox)
    maxx = max(b[2] for b in all_bbox)
    maxy = max(b[3] for b in all_bbox)
    bbox = [minx, miny, maxx, maxy]
    print("Gesamt-BBox:", bbox)

    # LV95 -> WGS84
    transformer = Transformer.from_crs("EPSG:2056", "EPSG:4326", always_xy=True)
    min_lon, min_lat = transformer.transform(minx, miny)
    max_lon, max_lat = transformer.transform(maxx, maxy)
    bbox_wgs84 = [min_lon, min_lat, max_lon, max_lat]
    print("BBox in WGS84:", bbox_wgs84)

    print("Querying swisstopo STAC API...")
    tiff_urls = query_stac(bbox_wgs84)

    print("Downloading orthophotos...")
    tiff_paths = download_files(tiff_urls, WORKDIR)

    print("Merging orthophotos...")
    merge_tiffs(tiff_paths, ORTHO_MERGED)

    # Colorize jede Punktwolke einzeln
    for pc in valid_pointclouds:
        print("Checking CRS:", pc)
        check_crs(pc)
        filename = os.path.basename(pc)
        output_file = os.path.join(downloads, f"colored_{filename}")
        print("Colorizing:", pc, "->", output_file)
        colorize_laz(pc, ORTHO_MERGED, output_file)

    print("Done! Output:", OUTPUT_LAZ)
