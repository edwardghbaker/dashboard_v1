import streamlit as st
import pandas as pd

location_df = pd.read_pickle(r'C:/Users/User/Documents/GitHub/dashboard_v1/data/locations.pkl')

st.header('Map of the Locations')

st.map(location_df,latitude='lat',longitude='lon',use_container_width=True)