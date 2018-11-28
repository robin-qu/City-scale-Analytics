import json
import pandas as pd


def json2csv():
    with open('data_table/park_only_boundary1.geojson') as f:
        data = json.load(f)
    
    df = pd.DataFrame(columns=['ID', 'name', 'coordinates'])
    
    id = 0;
    for feature in data['features']:
        id += 1
        if (feature['geometry']['coordinates']):
            df.loc[df.shape[0]] = [id,
                                   feature['properties']['name'],
                                   feature['geometry']['coordinates'][0][0]]
        else:
            print(id)
      
    filename = "data_table/park_only_boundary1.csv"
    df.to_csv(filename,  encoding='utf-8')

def main():
    json2csv()
    
if __name__ == '__main__':
    main()