#%%
import streamlit as st
st.set_page_config(layout="wide")
import pandas as pd
import os

location_df = pd.read_pickle(os.getcwd().split('dashboard_v1')[0]+'dashboard_v1\\data\\locations.pkl')
location_df.drop(10,inplace=True)
st.header('Map of the Locations')

col1,col2 = st.columns([3,1])

col2.subheader('Layers')
surface_data = col2.checkbox('Surface Water Data',value=True)
ground_data = col2.checkbox('Ground Water Data',value=True)

if surface_data and ground_data:
    col1.map(location_df[location_df['Type'].str.contains('Surface|Ground')],latitude='lat',longitude='lon',use_container_width=True,zoom=7)
elif surface_data:
    col1.map(location_df[location_df['Type'].str.contains('Surface')],latitude='lat',longitude='lon',use_container_width=True,zoom=7)
elif ground_data:
    col1.map(location_df[location_df['Type'].str.contains('Ground')], latitude='lat', longitude='lon', use_container_width=True, zoom=7)
# %%
