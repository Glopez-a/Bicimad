##############################################################################
#                                                                            #                       
#   argparse — Parser for command-line options, arguments and sub-commands   #     
#                                                                            #
#   Ironhack Data Part Time --> Feb-2023                                    #
#                                                                            #
##############################################################################


# import library

from dotenv import dotenv_values
import argparse
from modules import acquisition as imp
from modules import wrangling as wra
from modules import visualization as vis


# Argument parser function

def argument_parser():
    parser = argparse.ArgumentParser(description= 'Application for arithmetic calculations' )
    help_message1 ='Utiliza la opción -p ["Nombre del lugar"] para especificar el nombre del centro deportivo. Te devolverá la dirección de la estación más cercana a ese centro deportivo'
    help_message2 ='Utiliza la opción -n cuando no quieras especificar el nombre del centro deportivo. Se creará una tabla con las estaciones de Bicimad más cercanas a cada centro deportivo'
    
    parser.add_argument('-p', '--place', help=help_message1, type=str)
    parser.add_argument('-n', '--noplace', help=help_message2, action='store_true')

    args = parser.parse_args()
    return args

# input data

config = dotenv_values(".env")

DB_PATH = config['DB_PATH']
API_PATH = config['API_PATH']

command = argument_parser()
# Pipeline execution

print(API_PATH)

if __name__ == '__main__':
    if (command.noplace == True):
        df_raw_bici = imp.import_bicis(DB_PATH)
        df_clean_bici = wra.clean_bicis(df_raw_bici)
        json_raw_dep = imp.import_deps(API_PATH)
        df_clean_dep = wra.clean_deps(json_raw_dep)
        vis.plot_function(df_clean_bici, df_clean_dep)
        column = vis.closest_column(df_clean_dep, df_clean_bici)
        df_result = vis.create_complete_dataframe(column, df_clean_dep)
        print(df_result)
    elif (command.place != None):
        df_raw_bici = imp.import_bicis(DB_PATH)
        df_clean_bici = wra.clean_bicis(df_raw_bici)
        json_raw_dep = imp.import_deps(API_PATH)
        df_clean_dep = wra.clean_deps(json_raw_dep)
        df_clean_special_dep = wra.clean_special_deps(df_clean_dep, command.place)
        if (len(df_clean_special_dep) == 0):
            result = 'No existe ninguna instalación deportiva con un nombre parecido!'
            print(result)
        else:
            vis.plot_function(df_clean_bici, df_clean_special_dep)
            column = vis.closest_column(df_clean_special_dep, df_clean_bici)
            df_result = vis.create_complete_dataframe(column, df_clean_special_dep)
            print(df_result)
    else:
        result = 'FATAL ERROR...you need to select the correct method'
        print(result)
