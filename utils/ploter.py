"""
Filename: ploter.py
Author: Yassin Rhouma & Chantal Fuchs
Date: 2025-03-21
Description: This file contains all the function definitions for any plots in the dashboard.
Version: 1.0
License: MIT 
"""

import pandas as pd 
import geopandas as gpd
import plotly.express as px 


######################################################################################################################

def plot_density_map(df):
    fig = px.density_map(df, lat='latitude', lon='longitude', radius=10,
                        center=dict(lat=47.37733, lon=8.540068), zoom=12,
                        map_style="open-street-map")
    fig.update_layout(height=800, width=800)
    
    return fig

if __name__ == '__main__':
    pass