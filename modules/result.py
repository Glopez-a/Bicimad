from modules import geo_calculations as geo
import pandas as pd
import matplotlib.pyplot as plt
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

def closest_point(lat, long, df):
    dist_min = 500000
    point = ""
    for i, j in df.iterrows():
        dist = geo.distance_meters(lat, long, j[1], j[2])[0]
        if (dist < dist_min):
            dist_min = dist
            point = j
    return point

def extract_rows(df, lat, long):
    return df.loc[abs(df['latitud'] - lat) ** 2 + abs(df['longitud'] - long) ** 2 < 0.0065].reset_index(drop=True)

def closest_column(df_dep, df_bici):
    return [closest_point(df_dep.iloc[i][2], df_dep.iloc[i][3],
                extract_rows(df_bici, df_dep.iloc[i][2], df_dep.iloc[i][3])) for i in range(len(df_dep))]
      
def create_complete_dataframe(column, df_clean_dep):
    df_result = df_clean_dep[['Name', 'Type of place', 'Address']].copy()
    df_result['Bicimad Station'] = [i[0] for i in column]
    df_result['Station Location'] = [i[3] for i in column]
    df_result.to_csv("./data/result1.csv", index=False)
    return df_result

def process_place(place, df_deps, df_bicis):
    close_places = []

    for i, row in df_deps.iterrows():
        if fuzz.partial_ratio(row['Name'], place) > 80:
            serie = closest_point(row['Latitud'], row['Longitud'], df_bicis)
            serie['NameDep'] = row[0]
            serie['Address'] = row[4]
            close_places.append(serie)
    if len(close_places) == 0:
        return None
    return close_places

def create_special_dataframe(columns):
    deps = [i['NameDep'] for i in columns]
    address = [i['Address'] for i in columns]
    bicis = [i['name'] for i in columns]
    bici_address = [i['Station Location'] for i in columns]
    df_result = pd.DataFrame({'Name': deps, 'Address': address,
        'Bicimad Station': bicis, 'Station Location': bici_address})
    df_result.to_csv("./data/special_result.csv", index=False)
    return df_result


