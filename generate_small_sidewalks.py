# This program extracts paths in Greenlake area and saves in a csv file

import csv
import pandas as pd

upper = 47.6868735
lower = 47.6649775
left = -122.354941
right = -122.317496

def make_small_sw_csv():
    """
    Extracts all the sidwalks around green lake area, stores 
    in a new csv file.
    """
    df = pd.DataFrame(columns=['id', 'forward', 'incline', 'layer', 'side',
                               'street_name', 'surface', 'width', 'length',
                               'v_coordinates', 'u_coordinates'])
    file = open('data_table/sidewalks.csv')
    for row in csv.DictReader(file):
        v = row["v_coordinates"][1: -1].split(',')
        xv = float(v[0])
        yv = float(v[1])
        u = row["u_coordinates"][1: -1].split(',')
        xu = float(u[0])
        yu = float(u[1])
        condition1 = left <= xv <= right and left <= xu <= right
        condition2 = lower <= yv <= upper and lower <= yu <= upper
        if condition1 and condition2:
            df.loc[df.shape[0]] = [row['ID'],
                                   row['forward'],
                                   row['incline'],
                                   row['layer'],
                                   row['side'],
                                   row['street_name'],
                                   row['surface'],
                                   row['width'],
                                   row['length'],
                                   [xv, yv],
                                   [xu, yu]]
    df.to_csv('data_table/small_sidewalks.csv',  encoding='utf-8')
    file.close()

def main():
    make_small_sw_csv()
    
if __name__ == '__main__':
    main()