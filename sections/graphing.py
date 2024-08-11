#%%
import streamlit as st
import pandas as pd
import plotly.express as px

#%%
swq = pd.read_pickle(r'C:/Users/User/Documents/GitHub/dashboard_v1/data/swq.pkl')
gwq = pd.read_pickle(r'C:/Users/User/Documents/GitHub/dashboard_v1/data/gwq.pkl')

# %%


st.title('Water Quality Dashboard')

#Make selector for the data
data_type = st.selectbox('Select the data type:', ['Surface Water', 'Ground Water'])

if data_type == 'Surface Water':
    data = swq
elif data_type == 'Ground Water':
    data = gwq

x_element = st.selectbox('Select the x-axis element:', data.columns)
y_element = st.selectbox('Select the y-axis element:', data.columns)

st.plotly_chart(px.scatter(data, x=x_element, y=y_element, title=f'{data_type} Quality'))