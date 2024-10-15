#%%
from json import tool
from tkinter import font
from turtle import ondrag
from numpy import size
import streamlit as st
#st.set_page_config(layout="wide")
import pandas as pd
import geopandas as gpd
import os
import pydeck as pdk
import json
import datetime as dt
import plotly.express as px

location_df = pd.read_pickle(os.getcwd().split('dashboard_v1')[0]+'dashboard_v1\\data\\locations.pkl')
location_df.drop(10, inplace=True)

swq = pd.read_pickle(os.getcwd().split('dashboard_v1')[0]+'dashboard_v1\\data\\swq.pkl')
gwq = pd.read_pickle(os.getcwd().split('dashboard_v1')[0]+'dashboard_v1\\data\\gwq.pkl')

project_data = pd.DataFrame(columns=['lat', 'lon'],
                            data=[[-28.4359, -69.5486]])

FL_data = json.load(open(os.getcwd().split('dashboard_v1')[0]+'dashboard_v1\\data\\facilityline_2d.json'))
GA_data = json.load(open(os.getcwd().split('dashboard_v1')[0]+'dashboard_v1\\data\\GA_2d.json'))
HR_data = json.load(open(os.getcwd().split('dashboard_v1')[0]+'dashboard_v1\\data\\haulroad_2d.json'))
RA_data = json.load(open(os.getcwd().split('dashboard_v1')[0]+'dashboard_v1\\data\\roadaccess_2d.json'))
TR_data = json.load(open(os.getcwd().split('dashboard_v1')[0]+'dashboard_v1\\data\\tempaccessroad_2d.json'))
TC_data = json.load(open(os.getcwd().split('dashboard_v1')[0]+'dashboard_v1\\data\\transmissionline_chain_2d.json'))
TL_data = json.load(open(os.getcwd().split('dashboard_v1')[0]+'dashboard_v1\\data\\transmissionline_line_2d.json'))


col1, col2 = st.columns([4, 1])

layer_expander = col2.expander('Map Layers', expanded=True)
layer_expander.subheader('Data Layers')
surface_data = layer_expander.checkbox('Surface Water Data', value=True)
ground_data = layer_expander.checkbox('Ground Water Data', value=True)
names_on_map = layer_expander.checkbox('Show Names', value=False)
layer_expander.subheader('Facility Layers')
facilities = layer_expander.checkbox('Facility Line', value=True)
roads = layer_expander.checkbox('Roads', value=True)
powerlines = layer_expander.checkbox('Powerlines', value=True)


plotting_expander = col2.expander('Plotting Settings', expanded=False)
value_for_column_plot = plotting_expander.selectbox('Select the analyte for plotting', [None]+[i for i in list(gwq.columns.intersection(swq.columns)) if i not in ['SITE ID', 'Date']])
domain_radio = plotting_expander.radio('Select domian', ['Surface', 'Both', 'Ground'])
result_radio = plotting_expander.radio('Select plotting stat', ['Mean', 'Median', 'Max'])
dates = plotting_expander.date_input("Select date range",
                                     (dt.date(1900,1,1), dt.date(2100, 12, 31)),
                                     None,
                                     None,
                                     format="DD.MM.YYYY")

timeseries_expander = col2.expander('Time Series Settings', expanded=False)
# col2

FL = pdk.Layer(
                'GeoJsonLayer',
                data=FL_data,
                id='facilityline-layer',
                pickable=True,
                stroked=True,
                filled=True,
                extruded=False,
                get_fill_color='[255,255,255, 255]',
                get_line_color=[201, 144, 117],
                get_radius=10,
                opacity=1,
                get_elevation=0,
                get_line_width=10) # Facilities Line

GA = pdk.Layer(
                'GeoJsonLayer',
                data=GA_data,
                id='generalarrangement-layer',
                filled=True,
                extruded=False,
                get_fill_color='[161, 159, 159]',
                get_line_color=[0,0,1],
                get_radius=1,
                opacity=1,
                get_elevation=0,
                get_line_width=50) # General Arrangements 

HR = pdk.Layer(
                'GeoJsonLayer',
                data=HR_data,
                id='haulroad-layer',
                filled=True,
                extruded=False,
                get_fill_color='[255,255,255, 255]',
                get_line_color=[201, 144, 117],
                get_radius=10,
                opacity=1,
                get_elevation=0,
                get_line_width=10) # Haul Road

RA = pdk.Layer(
                'GeoJsonLayer',
                id='roadaccess-layer',
                data=RA_data,
                pickable=True,
                stroked=True,
                filled=False,
                extruded=False,
                get_fill_color='[255,255,255, 255]',
                get_line_color=[201, 144, 117],
                get_radius=10,
                opacity=1,
                get_elevation=0,
                get_line_width=10) # Road Access

TR = pdk.Layer(
                'GeoJsonLayer',
                data=TR_data,
                id='tempaccessroad-layer',
                pickable=True,
                stroked=True,
                filled=False,
                extruded=False,
                get_fill_color='[255,255,255, 255]',
                get_line_color=[201, 144, 117],
                get_radius=10,
                opacity=1,
                get_elevation=0,
                get_line_width=10) # Temporary Access Road

TC = pdk.Layer(
                'GeoJsonLayer',
                data=TC_data,
                id='transmissionchain-layer',
                pickable=True,
                stroked=True,
                filled=False,
                extruded=False,
                get_fill_color='[0, 0, 0, 200]',
                get_line_color=[120, 28, 28],
                get_radius=10,
                opacity=1,
                get_elevation=0,
                get_line_width=75) # Transmission Chain

TL = pdk.Layer(
                'GeoJsonLayer',
                data=TL_data,
                id='transmission-line',
                pickable=True,
                stroked=True,
                filled=False,
                extruded=False,
                get_fill_color='[0, 0, 0, 200]',
                get_line_color=[120, 28, 28],
                get_radius=10,
                opacity=1,
                get_elevation=0,
                get_line_width=10) # Transmission Line

surface_layer = pdk.Layer(
    'ScatterplotLayer',
    data=location_df[location_df['Type'].str.contains('Surface')],
    id='surface-layer',
    get_position='[lon, lat]',
    get_color='[115, 191, 48, 160]',
    get_radius=100,
)
ground_layer = pdk.Layer(
    'ScatterplotLayer',
    data=location_df[location_df['Type'].str.contains('Ground')],
    id='ground-layer',
    get_position='[lon, lat]',
    get_color='[53, 48, 191, 160]',
    get_radius=100,
)

if names_on_map:
    df_names = pd.DataFrame()
    if surface_data:
        df_names = pd.concat([df_names, location_df[location_df['Type'].str.contains('Surface')]])
    if ground_data:
        df_names = pd.concat([df_names, location_df[location_df['Type'].str.contains('Ground')]])

    name_layer = pdk.Layer(
        'TextLayer',
        data=df_names,
        id='text-layer',
        get_position='[lon, lat]',
        get_text='Name',
        get_size=12,
        get_color='[0, 0, 0, 255]',
        get_angle=0,
    )

if value_for_column_plot:
    #Get the dataset
    if domain_radio == 'Surface':
        df = swq
        location_df = location_df[location_df['Type'].str.contains(domain_radio)]
    elif domain_radio == 'Ground':
        df = gwq
        location_df = location_df[location_df['Type'].str.contains(domain_radio)]
    else:
        df = pd.concat([swq, gwq])
    
    df = df[list(gwq.columns.intersection(swq.columns))] #Ensure only valid columns are present
    df = df[(df['Date'] >= pd.to_datetime(dates[0])) & (df['Date'] <= pd.to_datetime(dates[1]))] #Filter by date # type: ignore
    df = df.groupby('SITE ID').agg(result_radio.lower()) #Aggregate by result # type: ignore

    #Merge the data with the location data
    column_df = location_df.merge(df, left_on='Name', right_on='SITE ID', how='left')

    column_df = column_df[['Name','lat', 'lon', value_for_column_plot]]
    column_df.columns = ['SITE ID','lat', 'lon', 'value']
    column_df['value'] = 1000*column_df['value']/column_df['value'].max()

    barplot_layer = pdk.Layer(
        'ColumnLayer',
        id='column-layer',
        data=column_df,
        get_position='[lon, lat]',
        get_elevation='value',
        get_color='[100, 200, 200, 255]',
        radius=100,
        pickable=True,
    )
    scatter_layer = pdk.Layer(
        'ScatterplotLayer',
        data=column_df,
        id='scatter-layer',
        get_position='[lon, lat]',
        get_color='[100, 200, 200, 255]',
        get_radius='value',
        pickable=True,
        tooltip=True,
    )
# Define the view state
view_state = pdk.ViewState(
    latitude=location_df['lat'].mean(),
    longitude=location_df['lon'].mean(),
    zoom=10,
    pitch=50,
)
layers_to_plot = []

if facilities:
    layers_to_plot.append(GA)
if roads:
    layers_to_plot.append(HR)
    layers_to_plot.append(RA)
    layers_to_plot.append(TR)
    layers_to_plot.append(FL)
if powerlines:
    layers_to_plot.append(TC)
    layers_to_plot.append(TL)
if surface_data:
    layers_to_plot.append(surface_layer)
if ground_data:
    layers_to_plot.append(ground_layer)
if names_on_map:
    layers_to_plot.append(name_layer)
if value_for_column_plot:
    layers_to_plot.append(scatter_layer)

chart = pdk.Deck(
                layers=layers_to_plot, 
                initial_view_state=view_state, 
                map_style='light', 
                height=1400,
                tooltip=True
                )

# Render the deck.gl map with the GeoJSON layer
event = col1.pydeck_chart(chart, 
                          use_container_width=True,
                          on_select="rerun", 
                          selection_mode="multi-object")

if event and value_for_column_plot:
    idx_list = event.selection.get('indices').get('scatter-layer') # type: ignore

    quick_plot = px.scatter(swq.loc[swq['SITE ID'].isin(column_df.loc[idx_list,'SITE ID'])],
                            x='Date',
                            y=value_for_column_plot,
                            color='SITE ID')
    col1.plotly_chart(quick_plot)
