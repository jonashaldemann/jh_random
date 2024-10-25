

def remove_all_duplicates_and_get_indices(curves, tolerance=0.01):
    duplicate_indices = []  # Liste der Indexpaarungen von Duplikaten
    unique_curves = []      # Liste der eindeutigen Kurven
    indices_to_remove = set()

    for i in range(len(curves)):
        current_curve = curves[i]
        current_duplicates = [i]  # Enthält den Index der aktuellen Kurve

        for j in range(i + 1, len(curves)):
            compare_curve = curves[j]
            # Überprüfen, ob die Kurven als Duplikate betrachtet werden
            if abs(current_curve.GetLength() - compare_curve.GetLength()) < tolerance:
                if current_curve.PointAtStart.DistanceTo(compare_curve.PointAtStart) < tolerance and \
                   current_curve.PointAtEnd.DistanceTo(compare_curve.PointAtEnd) < tolerance:
                    # Wenn sie Duplikate sind, speichern wir den Index der vergleichenden Kurve
                    current_duplicates.append(j)
                    indices_to_remove.add(i)
                    indices_to_remove.add(j)

        # Wenn mehrere Duplikate gefunden wurden, speichern wir sie in der Liste
        if len(current_duplicates) > 1:
            duplicate_indices.append(current_duplicates)

    # Entferne alle Kurven, deren Indizes in indices_to_remove sind
    unique_curves = [curve for i, curve in enumerate(curves) if i not in indices_to_remove]

    return unique_curves, duplicate_indices

# Beispiel: Eingabeparameter
tolerance = 0.01  # Toleranzwert für die Erkennung

# Aufrufen der Funktion
unique_curves, duplicate_indices = remove_all_duplicates_and_get_indices(Centerline, tolerance)

# Ausgabe
a = unique_curves         # Liste der eindeutigen Kurven
b = duplicate_indices     # Liste der Indexpaarungen der Duplikate

unique_vectors = ZVector

for group in duplicate_indices:
    unique_curves.append(Centerline[group[0]])
    v1 = ZVector[group[0]]
    v2 = ZVector[group[1]]
    vx = v1 + v2
    unique_vectors.append(vx)

all_indices = []
for index in duplicate_indices:
    for i in index:
        all_indices.append(i)

for i in all_indices:
    del unique_vectors[i]

C = unique_curves
V = unique_vectors