#%%
import streamlit as st
#st.set_page_config(layout="wide")

import pandas as pd
import plotly.express as px
import os

from traitlets import default
#%%

swq = pd.read_pickle(os.getcwd().split('dashboard_v1')[0]+'dashboard_v1\\data\\swq.pkl')
gwq = pd.read_pickle(os.getcwd().split('dashboard_v1')[0]+'dashboard_v1\\data\\gwq.pkl')

# %%

#st.title('Water Quality Dashboard')
col1, col2 = st.columns([3, 1])

#Make selector for the data
data_type = col2.selectbox('Select the data type:', ['Surface Water', 'Ground Water'])

if data_type == 'Surface Water':
    data = swq
elif data_type == 'Ground Water':
    data = gwq

# Add date selector
start_date = col2.date_input('Start date', value=pd.to_datetime('2000-01-01'))
end_date = col2.date_input('End date', value=pd.to_datetime('2023-12-31'))

# Filter data based on date range
data = data[(data['Date'] >= pd.to_datetime(start_date)) & (data['Date'] <= pd.to_datetime(end_date))] # type: ignore

default_y = list(data.columns).index('SITE ID')
y_element = col2.selectbox('Y element', data.columns, index=default_y)
default_x = list(data.columns).index('Date')
x_element = col2.selectbox('X element', data.columns, index=default_x)
columns_needed = [x_element, y_element]

color_map = None
color_by = col2.selectbox('Select the color element:', [None]+list(data.columns))
if color_by:
    color_map = col2.selectbox('Select the color map:', px.colors.named_colorscales())
    columns_needed.append(color_by)

size_by = col2.selectbox('Select the size element:', [None]+list(data.columns))
if size_by:
    columns_needed.append(size_by)

df_to_plot = data[columns_needed].dropna()

col1.plotly_chart(
    px.scatter(df_to_plot,
               x=x_element, 
               y=y_element, 
               color=color_by, 
               size=size_by, 
               color_continuous_scale=color_map, 
               height=700), 
    use_container_width=True, )
# %%
