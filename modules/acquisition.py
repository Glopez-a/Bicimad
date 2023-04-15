import duckdb
import pandas as pd
import requests
import json


def import_bicis(path):
    conn = duckdb.connect(path, read_only=True)
    df = conn.execute('SELECT name, "geometry.coordinates" AS Coordinates,\
                       address AS "Station Location"  FROM bicimad_stations').fetch_df()
    df.to_csv("./data/raw_bicis.csv", index=False)
    return df

def import_deps(path):
    response = requests.get('https://datos.madrid.es/egob' + path).json()
    centers = response['@graph']
    with open('./data/raw_deps.json', 'w') as f:
        json.dump(centers, f)
    return centers