#%%
import streamlit as st
st. set_page_config(layout="wide")
import pandas as pd
import plotly.express as px
import os
#%%

swq = pd.read_pickle(os.getcwd().split('dashboard_v1')[0]+'dashboard_v1\\data\\swq.pkl')
gwq = pd.read_pickle(os.getcwd().split('dashboard_v1')[0]+'dashboard_v1\\data\\gwq.pkl')

# %%

st.title('Water Quality Dashboard')
col1, col2 = st.columns([3, 1])

#Make selector for the data
data_type = col2.selectbox('Select the data type:', ['Surface Water', 'Ground Water'])

if data_type == 'Surface Water':
    data = swq
elif data_type == 'Ground Water':
    data = gwq

# Add date selector
start_date = col2.date_input('Start date', value=pd.to_datetime('2022-01-01'))
end_date = col2.date_input('End date', value=pd.to_datetime('2022-12-31'))

# Filter data based on date range
data = data[(data['Date'] >= pd.to_datetime(start_date)) & (data['Date'] <= pd.to_datetime(end_date))]

y_element = col2.selectbox('Select the y-axis element:', data.columns)
x_element = col2.selectbox('Select the x-axis element:', data.columns)


col1.plotly_chart(px.scatter(data, x=x_element, y=y_element, title=f'{data_type} Quality'))
# %%
