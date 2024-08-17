#%%
import streamlit as st
st.set_page_config(layout="wide")
import pandas as pd
import os
import pydeck as pdk

location_df = pd.read_pickle(os.getcwd().split('dashboard_v1')[0]+'dashboard_v1\\data\\locations.pkl')
location_df.drop(10, inplace=True)

project_data = pd.DataFrame(columns=['lat', 'lon'],
                            data=[[-28.4359, -69.5486]])

st.header('Map of the Locations')

col1, col2 = st.columns([3, 1])

col2.subheader('Layers')
surface_data = col2.checkbox('Surface Water Data', value=True)
ground_data = col2.checkbox('Ground Water Data', value=True)
col2.subheader('Settings')

# Define a GeoJSON layer
geojson_layer = pdk.Layer(
    'GeoJsonLayer',
    data='https://raw.githubusercontent.com/visgl/deck.gl-data/master/examples/geojson/vancouver-blocks.json',
    pickable=True,
    stroked=False,
    filled=True,
    extruded=True,
    get_fill_color='[255, 255, 255, 200]',
    get_line_color=[255, 255, 255],
    get_radius=200,
)

# Define the view state
view_state = pdk.ViewState(
    latitude=location_df['lat'].mean(),
    longitude=location_df['lon'].mean(),
    zoom=7,
    pitch=50,
)

# Render the deck.gl map with the GeoJSON layer
col1.pydeck_chart(pdk.Deck(layers=[geojson_layer], initial_view_state=view_state))

if surface_data and ground_data:
    col1.map(location_df[location_df['Type'].str.contains('Surface|Ground')], latitude='lat', longitude='lon', use_container_width=True, zoom=7)
elif surface_data:
    col1.map(location_df[location_df['Type'].str.contains('Surface')], latitude='lat', longitude='lon', use_container_width=True, zoom=7)
elif ground_data:
    col1.map(location_df[location_df['Type'].str.contains('Ground')], latitude='lat', longitude='lon', use_container_width=True, zoom=7)
