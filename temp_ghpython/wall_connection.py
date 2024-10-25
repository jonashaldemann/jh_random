import ghpythonlib.components as gh

class Wall:
    def __init__(self, surface, thickness):
        self.surface = surface
        self.thickness = thickness
        self.intersection_curves = []
        self.extension_vectors = []
        self.topologies = []
    
    def get_info(self):
        return self.surface, self.thickness
    
    def get_area(self):
        area, _ = gh.Area(self.surface)
        return area
    
    def print_info(self):
        return "Info"

    def extend(self, crv, thickness):
        _, centroid = gh.Area(self.surface)
        crv_middle = gh.CurveMiddle(crv)
        vector, _ = gh.Vector2Pt(centroid, crv_middle, True)
        vector = gh.Amplitude(vector, thickness)
        brep = gh.Extrude(crv, vector)
        brep_joined, _ = gh.BrepJoin([self.surface, brep])
        brep_merged, _, _, = gh.MergeFaces(brep_joined)
        self.surface = brep_merged


class Building:
    def __init__(self, walls):
        self.walls = walls
        self.connections = []
        self.calculate_connections()
    
    def get_info(self):
        return self.walls
    
    def calculate_connections(self):
        for i , wall_i in enumerate(self.walls):
            for wall_j in self.walls[i + 1:]: # Vermeide Doppelberechnung
                curve, _ = gh.BrepXBrep(wall_i.surface, wall_j.surface)
                if curve:
                    point = gh.CurveMiddle(curve)
                    topology_i = self._get_topology(point, wall_i.surface)
                    topology_j = self._get_topology(point, wall_j.surface)

                    connection_type = "L" if topology_i == "end" and topology_j == "end" else "T"
                    self.connections.append(WallConnection(wall_i, wall_j, curve, connection_type))
    
    @staticmethod
    def _get_topology(point, surface):
        _, uv, _ = gh.SurfaceClosestPoint(point, surface)
        u, v, z = uv
        u = round(u, 1)
        v = round(v, 1)

        if u == 0.5:
            position = v
        if v == 0.5:
            position = u

        if position == 0.0 or position == 1.0:
            return "end"
        else:
            return "mid"



class WallConnection():
    def __init__(self, wall1, wall2, intersection_crv, topology):
        self.wall1 = wall1
        self.wall2 = wall2
        self.intersection_crv = intersection_crv
        self.topology = topology

        if topology == "L":
            self.apply_l_extension()
    
    def apply_l_extension(self):
        self.wall1.extend(self.intersection_crv, self.wall2.thickness)