shift_y = -2663656.644003
shift_x = -1216472.779001
z_move = 0.000000

# Beispielverwendung
input_file = '/Users/jonashaldemann/Nextcloud2/Buero/013 WW Rothenburg/10 Archicad/_bestandteile/Geometerpunkte von ChatGPT.txt'
output_file = '/Users/jonashaldemann/Nextcloud2/Buero/013 WW Rothenburg/10 Archicad/_bestandteile/Geometerpunkte shifted.txt'

def read_points(file_path):
    points = []
    with open(file_path, 'r') as file:
        for line in file:
            x, y, z = map(float, line.strip().split())
            points.append((x, y, z))
    return points

def shift_points(points, shift_x, shift_y):
    shifted_points = []
    for x, y, z in points:
        shifted_points.append((x + shift_x, y + shift_y, z))
        print(x, y)
        print(shift_x, shift_y)
        print(x + shift_x, y + shift_y, z)
    return shifted_points

def write_points(file_path, points):
    with open(file_path, 'w') as file:
        for x, y, z in points:
            file.write(f"{y},{x},{z}\n")



points = read_points(input_file)
shifted_points = shift_points(points, shift_x, shift_y)
write_points(output_file, shifted_points)