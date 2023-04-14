import duckdb
import pandas as pd
import re
import requests
import matplotlib.pyplot as plt
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

def clean_bicis(df):
    df['name'] = df['name'].str.replace('^(\S)* - ', '', regex=True)
    df['Station Location'] = df['Station Location'].str.replace(' nº', ',', regex=True)
    df['latitud'] = [float(df['Coordinates'][i].split(",")[1][:-1]) for i in range(len(df))]
    df['longitud'] = [float(df['Coordinates'][i].split(",")[0][1:-1]) for i in range(len(df))]
    df[['name', 'latitud', 'longitud', 'Station Location']].to_csv("./data/clean_bicis.csv", index=False)
    return df[['name', 'latitud', 'longitud', 'Station Location']]

def clean_deps(raw_json):
    title = [i['title'] for i in raw_json]
    loc_lat = [i['location']['latitude'] for i in raw_json]
    loc_long = [i['location']['longitude'] for i in raw_json]
    place = ["Instalación deportiva" for i in raw_json]
    address = [i['address']['street-address'].title() for i in raw_json]
    df_dep = pd.DataFrame({'Name': title, 'Type of place': place, 'Latitud': loc_lat, 'Longitud': loc_long, 'Address': address})
    df_dep.to_csv("./data/clean_deps.csv", index=False)
    return df_dep

#        if fuzz.partial_ratio(row['Name'], place) > 80:


def clean_special_deps(df, place):
    for i, row in df.iterrows():
        if (fuzz.partial_ratio(row['Name'], place) < 80):
            df.drop(i, inplace=True)
    return(df)

def plot_function(df_bicis, df_dep):
    plt.close("all")

    ax = df_bicis.plot.scatter(x="latitud", y="longitud", color="DarkBlue", label="Group Bicis stations")
    df_dep.plot.scatter(x="Latitud", y="Longitud", color="Yellow", label="Group Points of Interest", ax=ax)
    plt.savefig('./data/plot.png')