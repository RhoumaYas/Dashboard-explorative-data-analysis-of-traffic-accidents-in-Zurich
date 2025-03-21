"""
Filename: imports.py
Author: Yassin Rhouma & Chantal Fuchs
Date: 2025-03-21
Description: This file contains all the function definitions for any data imports and preprocessing tasks in the dashboard.
Version: 1.0
License: MIT 
"""

import streamlit as st 
import pandas as pd 
import numpy as np
import geopandas as gpd 
from typing import Optional


### Constants #####################################################################################################################
PATH_TO_ACCIDENT_DATA = 'https://data.stadt-zuerich.ch/dataset/sid_dav_strassenverkehrsunfallorte/download/RoadTrafficAccidentLocations.csv'
COLUMNS_TO_SELECT = [
                        'AccidentType_en', 
                        'AccidentSeverityCategory_en',
                        'AccidentInvolvingPedestrian', 
                        'AccidentInvolvingBicycle',
                        'AccidentInvolvingMotorcycle', 
                        'RoadType_en', 
                        'AccidentLocation_CHLV95_E',
                        'AccidentLocation_CHLV95_N',
                        'AccidentYear', 
                        'AccidentMonth_en',
                        'AccidentWeekDay_en', 
                        'AccidentHour'
                    ]

### Imports #####################################################################################################################

@st.cache_data()
def get_dataframe(path_to_dataframe: str) -> pd.DataFrame:
    df_raw = pd.read_csv(path_to_dataframe)
    return df_raw
    


def get_accident_data(path: Optional[str] = None) -> pd.DataFrame:
    if path:
        return get_dataframe(path)
    else:
        return get_dataframe(PATH_TO_ACCIDENT_DATA)
    

### Preprocessing #####################################################################################################################

def process_accident_data(dataframe: pd.DataFrame, columns: Optional[list] = None, parking: bool=False) -> pd.DataFrame:
    
    if not parking:
        filtered_df = dataframe[~dataframe['AccidentType_en'].str.contains('parking')]
    else:
        filtered_df = dataframe
        
    if columns:
        return filtered_df[columns]   
    else:
        return filtered_df[COLUMNS_TO_SELECT]
    


def convert_coordinate_reference_system(dataframe: pd.DataFrame, x_y: Optional[tuple]=None, crs_in: int=2056, crs_out: int=4326) -> pd.DataFrame:
    
    if x_y:
        gdf = gpd.GeoDataFrame(dataframe, geometry=gpd.points_from_xy(dataframe.x_y[0], dataframe.x_y[1]), crs=f'EPSG:{crs_in}')
        dataframe = dataframe.drop(x_y, axis=1)
    
    else:
        gdf = gpd.GeoDataFrame(dataframe, geometry=gpd.points_from_xy(dataframe.AccidentLocation_CHLV95_E, dataframe.AccidentLocation_CHLV95_N), crs=f'EPSG:{crs_in}')
        dataframe = dataframe.drop(['AccidentLocation_CHLV95_E', 'AccidentLocation_CHLV95_N'], axis=1)
        
    
    gdf = gdf.to_crs(4326)
    dataframe["longitude"] = gdf.geometry.x
    dataframe["latitude"] = gdf.geometry.y
    
    
    return dataframe



if __name__ == '__main__':
    pass