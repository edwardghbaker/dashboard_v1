#%%
import geopandas as gpd
from glob import glob
from shapely import force_2d
from icecream import ic

# %%

def geojson_to_2d_json(path:str):
    temp = gpd.read_file(path)
    temp = temp.to_crs(epsg=4326)

    temp['geometry'] = force_2d(temp['geometry'])
    new_path = path.replace('.geojson','_2d.json')
    temp.to_file(ic(new_path))

# %%

# for path in glob(r'..\data\*.geojson'):
#     geojson_to_2d_json(path)

#%% Hash passwords
from yaml.loader import SafeLoader
import yaml
import streamlit_authenticator as stauth
from streamlit_authenticator.utilities import Hasher
with open('../user_details.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)
#Pre-hashing all plain text passwords once
Hasher.hash_passwords(config['credentials'])
# %%
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

swq = pd.read_pickle(os.getcwd().split('dashboard_v1')[0]+'dashboard_v1\\data\\swq.pkl')
gwq = pd.read_pickle(os.getcwd().split('dashboard_v1')[0]+'dashboard_v1\\data\\gwq.pkl')

numeric_df = location_df.select_dtypes(include=['number'])
numeric_df_norm = 1000*(numeric_df-numeric_df.min())/(numeric_df.max()-numeric_df.min())
numeric_df_norm = numeric_df_norm.fillna(0)
numeric_df_norm['lat'] = location_df['lat']
numeric_df_norm['lon'] = location_df['lon']

# %%
