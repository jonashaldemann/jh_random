import ghpythonlib.components as gh

indexes = []
end_lines = []
extension_vectors = []

# Topologie analysieren 
for surface_i in surfaces:
    index_i = []
    end_line_i = []
    extension_vectors_i = []

    _, centroid_i = gh.Area(surface_i)
    for j, surface_j in enumerate(surfaces):
        int_crv, _ = gh.BrepXBrep(surface_i, surface_j)
        if int_crv:
            index_i.append(j)
            end_line_i.append(int_crv)
            curve_middle = gh.CurveMiddle(int_crv)
            vector, _ = gh.Vector2Pt(centroid_i, curve_middle, True)
            extension_vectors_i.append(vector)
       
    indexes.append(index_i)
    end_lines.append(end_line_i)
    extension_vectors.append(extension_vectors_i)

print(indexes)
print(end_lines)
print(extension_vectors)