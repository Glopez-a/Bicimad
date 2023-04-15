from modules import geo_calculations as geo
import pandas as pd
import matplotlib.pyplot as plt


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
    return df.loc[abs(df['latitud'] - lat) ** 2 + abs(df['longitud'] - long)\
                   ** 2 < 0.0065].reset_index(drop=True)

def closest_column(df_dep, df_bici):
    return [closest_point(df_dep.iloc[i][2], df_dep.iloc[i][3],
                extract_rows(df_bici, df_dep.iloc[i][2], df_dep.iloc[i][3])) for i in range(len(df_dep))]
      
def create_complete_dataframe(column, df_clean_dep):
    df_result = df_clean_dep[['Name', 'Type of place', 'Address']].copy()
    df_result['Bicimad Station'] = [i[0] for i in column]
    df_result['Station Location'] = [i[3] for i in column]
    df_result.to_csv("./data/result1.csv", index=False)
    return df_result



def create_special_dataframe(columns):
    deps = [i['NameDep'] for i in columns]
    address = [i['Address'] for i in columns]
    bicis = [i['name'] for i in columns]
    bici_address = [i['Station Location'] for i in columns]
    df_result = pd.DataFrame({'Name': deps, 'Address': address,
        'Bicimad Station': bicis, 'Station Location': bici_address})
    df_result.to_csv("./data/special_result.csv", index=False)
    return df_result


def plot_function(df_bicis, df_dep):
    plt.close("all")

    ax = df_bicis.plot.scatter(x="latitud", y="longitud", color="DarkBlue", label="Group Bicis stations")
    df_dep.plot.scatter(x="Latitud", y="Longitud", color="Yellow", label="Group Points of Interest", ax=ax)
    plt.savefig('./data/plot.png')