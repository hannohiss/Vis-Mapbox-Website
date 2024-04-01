import json
from pyproj import Transformer

def transform_coordinates(input_file, output_file):
    try:
        print("Starting transformation...")
        # Initialize the transformer
        transformer = Transformer.from_crs("EPSG:26986", "EPSG:4326", always_xy=True)
        print("Transformer initialized.")

        # Read the input file
        with open(input_file, 'r') as file:
            data = json.load(file)
        print("Input file read successfully.")

        # Process each feature
        for feature in data['features']:
            geom_type = feature['geometry']['type']
            coords = feature['geometry']['coordinates']
            
            if geom_type in ['Polygon', 'MultiPolygon']:
                for poly in coords:
                    for ring in poly:
                        for i, coord in enumerate(ring):
                            x, y = transformer.transform(coord[0], coord[1])
                            ring[i] = [x, y]
            elif geom_type in ['Point', 'MultiPoint', 'LineString', 'MultiLineString']:
                for i, coord in enumerate(coords):
                    x, y = transformer.transform(coord[0], coord[1])
                    coords[i] = [x, y]
            else:
                print(f"Unsupported geometry type: {geom_type}")
                raise ValueError("Geometry type not supported")
        print("Transformation complete.")

        # Write the output file
        with open(output_file, 'w') as file:
            json.dump(data, file)
        print("Output file written successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")

# After modifying the function, remember to call it with the correct file paths
print("Complete")


# Example usage
input_geojson_file = '/Users/hanno/Documents/_Studium/MIT2/Vis Final Project/MapBox/ma_municipalities.geojson'
output_geojson_file = '/Users/hanno/Documents/_Studium/MIT2/Vis Final Project/MapBox/ma_municipalities_degrees.geojson'

transform_coordinates(input_geojson_file, output_geojson_file)
