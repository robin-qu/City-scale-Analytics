# This program enlarges the boundray of Greenlake Park and finds sidewalks
# that have intersection with or are included in the park boundary. A new 
# column is added to the sidewalk.csv file which indicates whether the 
# sidewalk has intersection

import csv
import json
import matplotlib.pyplot as plt
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon


def generate_park_dictionary(park_file):
    '''
    Reads the park geojson file as a dictionary whose keys are names
    of parks and values are the coordinates of parks.
    '''
    park_dict = {}
    with open(park_file) as park_file:
        park_data = json.load(park_file)
    for feature in park_data['features']:
        properties = feature["properties"]
        name = properties['name']
        if name not in park_dict.keys():
            park_dict[name] = [feature['geometry']['coordinates']]
        else:
            print('duplicated!')
            park_dict[name].append(feature['geometry']['coordinates'])
    return park_dict


def find_adjacent_park(coordinates, enlarged_polygon_dict):
    '''
    Given a list of coordinates of a sidewalk and the enlarged 
    polygon dictionary, finds and returns a list of park polygons 
    that intersect or incorporate the sidewalk.
    '''
    result = []
    endpoint1 = Point(coordinates[0])
    endpoint2 = Point(coordinates[1])
    for key in enlarged_polygon_dict.keys():
        for polygon in enlarged_polygon_dict[key]:
            if polygon.contains(endpoint1) or polygon.contains(endpoint2):
                result.append(key)
    return result


def read_sidewalk(sidewalk_file, new_sidewalk_file, enlarged_polygon_dict):
    '''
    Reads sidewalk csv file; checks if each sidewalk is inside or 
    intersected with a park boundary (enlarged polygon), return a
    new csv file wiht a new column indicates a list of park the 
    sidewalk belongs to.
    '''
    with open(sidewalk_file, 'r') as csvinput:
        with open(new_sidewalk_file, 'w') as csvoutput:
            writer = csv.writer(csvoutput)
            reader = csv.reader(csvinput)
            
            content = []
            head = next(reader)
            head.append('adjacent_parks')
            content.append(head)
            
            for row in reader:
                coordinates = []
                coordinates.append([float(row[10][1: -1].split(',')[0]),
                                   float(row[10][1: -1].split(',')[1])])
                coordinates.append([float(row[11][1: -1].split(',')[0]),
                                   float(row[11][1: -1].split(',')[1])])
                row.append(find_adjacent_park(coordinates,
                                              enlarged_polygon_dict))
                content.append(row)
            
            writer.writerows(content)
            
        
#for key in park_dict.keys():
#    if len(park_dict[key]) > 1:
#        print(key, len(park_dict[key]))
            
            
park_dict = generate_park_dictionary('data_table/park_only_boundary1.geojson')

park_list = ['GREEN LAKE PARK', 'WOODLAND PARK ZOO', 'WOODLAND PARK',
         'LINDEN ORCHARD PARK', 'NE 60TH STREET PARK']
polygon_dict = {}
enlarged_polygon_dict = {}
for park in park_list:
    print(len(park_dict[park][0]))
    for i in range(len(park_dict[park][0])):
        coordiante = park_dict[park][0][i][0]
        polygon = Polygon(coordiante)
        if park not in polygon_dict.keys():
            polygon_dict[park] = [polygon]
        else:
            polygon_dict[park].append(polygon)
        x, y = polygon.exterior.xy
        plt.figure(1)
        plt.plot(x, y, 'k')
    
        enlarged_polygon = Polygon(polygon.buffer(0.0001).exterior)
        if park not in enlarged_polygon_dict.keys():
            enlarged_polygon_dict[park] = [enlarged_polygon]
        else:
            enlarged_polygon_dict[park].append(enlarged_polygon)
        x1, y1 = enlarged_polygon.exterior.xy
        plt.figure(1)
        plt.plot(x1, y1, 'b')
plt.show()
    
read_sidewalk('data_table/small_sidewalks.csv',
              'data_table/new_small_sidewalks.csv', enlarged_polygon_dict)
