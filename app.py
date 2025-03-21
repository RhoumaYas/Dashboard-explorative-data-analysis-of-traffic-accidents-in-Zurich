"""
Filename: app.py
Author: Yassin Rhouma & Chantal Fuchs
Date: 2025-03-21
Description: This file contains the main structure and functions the dashboard.
Version: 1.0
License: MIT 
"""

import streamlit as st 
from utils import imports, ploter 

st.set_page_config(page_title='Zurich Traffic Accident Dashboard', layout='wide', initial_sidebar_state='auto')

# Data imports ##################################################################################################################################

traffic_accident_data_raw = imports.get_accident_data()
traffic_accident_data_preprocessd = imports.process_accident_data(traffic_accident_data_raw)
traffic_accident_data_epsg4326 = imports.convert_coordinate_reference_system(traffic_accident_data_preprocessd)
final_traffic_df = traffic_accident_data_epsg4326.copy()




# st.write(final_traffic_df.columns)


###################################################################################################################################

st.header('Explorative Data Analysis Dashboard for Traffic Accidents in Zurich')



with st.sidebar:
    
    st.write('Select parameters')
    
    # select accident type:
    type_options = traffic_accident_data_epsg4326['AccidentType_en'].unique().tolist()
    with st.expander('Accident Type'):
        selected_types =  [opt for opt in type_options if st.checkbox(opt)]
        
        
    severity_options = traffic_accident_data_epsg4326['AccidentSeverityCategory_en'].unique().tolist()
    with st.expander('Accident Severity'):
        selected_severity =  [opt for opt in severity_options if st.checkbox(opt)]

    
    
    year_options = traffic_accident_data_epsg4326['AccidentYear'].unique().tolist()
   
    with st.expander('Accident Year'):
        selected_years =  [opt for opt in year_options if st.checkbox(str(opt))]
    
    month_options = traffic_accident_data_epsg4326['AccidentMonth_en'].unique().tolist()
    with st.expander('Accident Month'):
        selected_month =  [opt for opt in month_options if st.checkbox(str(opt))]

    with st.expander("Accident Weekday"):
        weekday_options = traffic_accident_data_epsg4326['AccidentWeekDay_en'].unique().tolist()
        selected_weekday = [opt for opt in weekday_options if st.checkbox(str(opt))]
    
    with st.expander('Accident Hour'):
        selected_hour = st.slider('Hour', 0, 23, value=(0,23) )
        
    with st.expander("Accident Involvement"):
        # st.write('Pedestrians:')
        pedestrian_options = traffic_accident_data_epsg4326['AccidentInvolvingPedestrian'].unique().tolist()
        selected_pedestrian = [opt for opt in pedestrian_options if st.checkbox('Pedestrians ' + str(opt))]
        # st.write('Bicycles:')
        bicycle_options = traffic_accident_data_epsg4326['AccidentInvolvingBicycle'].unique().tolist()
        selected_bicycle = [opt for opt in bicycle_options if st.checkbox('Bicycles ' + str(opt))]
        mbike_options = traffic_accident_data_epsg4326['AccidentInvolvingMotorcycle'].unique().tolist()
        selected_mbike = [opt for opt in mbike_options if st.checkbox('Motorcycles ' + str(opt))]

    with st.expander("Road Type"):
        road_options = traffic_accident_data_epsg4326['RoadType_en'].unique().tolist() 
        selected_road_type = [opt for opt in road_options if st.checkbox(str(opt)  + ' Road' if opt == 'Other' else str(opt))]



    filtered_final_df = final_traffic_df[
        (final_traffic_df['AccidentType_en'].isin(selected_types)) &
        (final_traffic_df['AccidentYear'].isin(selected_years)) &
        (final_traffic_df['AccidentMonth_en'].isin(selected_month)) &
        (final_traffic_df['AccidentHour'].isin(selected_hour)) &
        (final_traffic_df['AccidentSeverityCategory_en'].isin(selected_severity)) &
        (final_traffic_df['AccidentInvolvingPedestrian'].isin(selected_pedestrian)) &
        (final_traffic_df['AccidentInvolvingBicycle'].isin(selected_bicycle)) &
        (final_traffic_df['AccidentInvolvingMotorcycle'].isin(selected_mbike)) &
        (final_traffic_df['RoadType_en'].isin(selected_road_type)) &
        (final_traffic_df['AccidentWeekDay_en'].isin(selected_weekday))
    ]

fig = ploter.plot_density_map(filtered_final_df)
st.plotly_chart(fig)