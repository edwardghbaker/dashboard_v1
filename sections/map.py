#%%
import streamlit as st
#st.set_page_config(layout="wide")
import pandas as pd
import geopandas as gpd
import os
import pydeck as pdk
import json
import datetime as dt

location_df = pd.read_pickle(os.getcwd().split('dashboard_v1')[0]+'dashboard_v1\\data\\locations.pkl')
location_df.drop(10, inplace=True)

numeric_df = location_df.select_dtypes(include=['number'])
numeric_df_norm = 1000*(numeric_df-numeric_df.min())/(numeric_df.max()-numeric_df.min())
numeric_df_norm = numeric_df_norm.fillna(0)
numeric_df_norm['lat'] = location_df['lat']
numeric_df_norm['lon'] = location_df['lon']

project_data = pd.DataFrame(columns=['lat', 'lon'],
                            data=[[-28.4359, -69.5486]])

FL_data = json.load(open(os.getcwd().split('dashboard_v1')[0]+'dashboard_v1\\data\\facilityline_2d.json'))
GA_data = json.load(open(os.getcwd().split('dashboard_v1')[0]+'dashboard_v1\\data\\GA_2d.json'))
HR_data = json.load(open(os.getcwd().split('dashboard_v1')[0]+'dashboard_v1\\data\\haulroad_2d.json'))
RA_data = json.load(open(os.getcwd().split('dashboard_v1')[0]+'dashboard_v1\\data\\roadaccess_2d.json'))
TR_data = json.load(open(os.getcwd().split('dashboard_v1')[0]+'dashboard_v1\\data\\tempaccessroad_2d.json'))
TC_data = json.load(open(os.getcwd().split('dashboard_v1')[0]+'dashboard_v1\\data\\transmissionline_chain_2d.json'))
TL_data = json.load(open(os.getcwd().split('dashboard_v1')[0]+'dashboard_v1\\data\\transmissionline_line_2d.json'))

st.header('Map of the Locations')
col1, col2 = st.columns([3, 1])

col2.subheader('Layers')
surface_data = col2.checkbox('Surface Water Data', value=True)
ground_data = col2.checkbox('Ground Water Data', value=True)

col2.subheader('Settings')
names_on_map = col2.checkbox('Show Names', value=False)
values_for_column_plot = col2.selectbox('Select the column for the column plot', [None]+list(numeric_df_norm.columns))
dates = col2.date_input(
    "Select date range",
    (dt.date(2000,1,1), dt.date(2023, 12, 31)),
    None,
    None,
    format="DD.MM.YYYY")


FL = pdk.Layer(
                'GeoJsonLayer',
                data=FL_data,
                pickable=True,
                stroked=True,
                filled=False,
                extruded=False,
                get_fill_color='[0, 0, 0, 200]',
                get_line_color=[255, 0, 0],
                get_radius=100,
                opacity=1,
                get_elevation=0,
                get_line_width=50)

GA = pdk.Layer(
                'GeoJsonLayer',
                data=GA_data,
                pickable=True,
                stroked=True,
                filled=False,
                extruded=False,
                get_fill_color='[0, 0, 0, 200]',
                get_line_color=[0, 0, 0],
                get_radius=100,
                opacity=1,
                get_elevation=0,
                get_line_width=75)

HR = pdk.Layer(
                'GeoJsonLayer',
                data=HR_data,
                pickable=True,
                stroked=True,
                filled=False,
                extruded=False,
                get_fill_color='[0, 0, 0, 200]',
                get_line_color=[255, 0, 0],
                get_radius=100,
                opacity=1,
                get_elevation=0,
                get_line_width=75)

RA = pdk.Layer(
                'GeoJsonLayer',
                data=RA_data,
                pickable=True,
                stroked=True,
                filled=False,
                extruded=False,
                get_fill_color='[0, 0, 0, 200]',
                get_line_color=[255, 0, 0],
                get_radius=100,
                opacity=1,
                get_elevation=0,
                get_line_width=75)

TR = pdk.Layer(
                'GeoJsonLayer',
                data=TR_data,
                pickable=True,
                stroked=True,
                filled=False,
                extruded=False,
                get_fill_color='[0, 0, 0, 200]',
                get_line_color=[255, 0, 0],
                get_radius=100,
                opacity=1,
                get_elevation=0,
                get_line_width=75)

TC = pdk.Layer(
                'GeoJsonLayer',
                data=TC_data,
                pickable=True,
                stroked=True,
                filled=False,
                extruded=False,
                get_fill_color='[0, 0, 0, 200]',
                get_line_color=[255, 0, 0],
                get_radius=100,
                opacity=1,
                get_elevation=0,
                get_line_width=75)

TL = pdk.Layer(
                'GeoJsonLayer',
                data=TL_data,
                pickable=True,
                stroked=True,
                filled=False,
                extruded=False,
                get_fill_color='[0, 0, 0, 200]',
                get_line_color=[0, 0, 0],
                get_radius=100,
                opacity=1,
                get_elevation=0,
                get_line_width=50)

surface_layer = pdk.Layer(
    'ScatterplotLayer',
    data=location_df[location_df['Type'].str.contains('Surface')],
    get_position='[lon, lat]',
    get_color='[200, 30, 0, 160]',
    get_radius=100,
)
ground_layer = pdk.Layer(
    'ScatterplotLayer',
    data=location_df[location_df['Type'].str.contains('Ground')],
    get_position='[lon, lat]',
    get_color='[30, 200, 0, 160]',
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
        get_position='[lon, lat]',
        get_text='Name',
        get_size=12,
        get_color='[0, 0, 0, 255]',
        get_angle=0,
    )

if values_for_column_plot:

    # if dates is not None:
    #     numeric_df_norm = numeric_df_norm[(numeric_df_norm.index >= dates[0]) & (numeric_df_norm.index <= dates[1])]
    column_df = numeric_df_norm[['lat', 'lon', values_for_column_plot]]
    column_df.columns = ['lat', 'lon', 'value']

    
    
    barplot_layer = pdk.Layer(
        'ColumnLayer',
        data=column_df,
        get_position='[lon, lat]',
        get_elevation='value',
        get_color='[100, 200, 200, 255]',
        radius=100,
        pickable=True,
    )

# Define the view state
view_state = pdk.ViewState(
    latitude=location_df['lat'].mean(),
    longitude=location_df['lon'].mean(),
    zoom=10,
    pitch=50,
)
layers_to_plot = [FL,GA,HR,RA,TR,TL,TC]

if surface_data:
    layers_to_plot.append(surface_layer)
if ground_data:
    layers_to_plot.append(ground_layer)
if names_on_map:
    layers_to_plot.append(name_layer)
if values_for_column_plot:
    layers_to_plot.append(barplot_layer)

# Render the deck.gl map with the GeoJSON layer
col1.pydeck_chart(pdk.Deck(layers=layers_to_plot, initial_view_state=view_state, map_style='light'))

# %%
