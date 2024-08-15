import streamlit as st
st.set_page_config(layout="wide")
from util.PCA_func import perform_pca
import os
import pandas as pd
import plotly.express as px
#%%

swq = pd.read_pickle(os.getcwd().split('dashboard_v1')[0]+'dashboard_v1\\data\\swq.pkl')
gwq = pd.read_pickle(os.getcwd().split('dashboard_v1')[0]+'dashboard_v1\\data\\gwq.pkl')

st.header('Principal Component Analysis')

dataset = st.radio('Select Dataset', ['Ground Water Quality', 'Surface Water Quality'])

if dataset == 'Ground Water Quality':
    df = gwq
elif dataset == 'Surface Water Quality':
    df = swq
else:
    df = None


if df is not None:
    components = st.multiselect('Select the columns to be used as principal components', df.columns)
    num_pcs = st.number_input('Select the number of Principal Components to be calculated', min_value=1, max_value=len(components), value=3, step=1)
    pcs = st.multiselect('Select Principal Components to be plotted', [i for i in range(1, num_pcs+1)])

    principal_df, vectors, X_recreated = perform_pca(df, components, pcs, plot=False)


    if len(pcs) == 1:
        st.plotly_chart(px.histogram(principal_df, x=f'PC{pcs[0]}'), use_container_width=True)
    elif len(pcs) == 2:
        st.plotly_chart(px.scatter(principal_df, x=f'PC{pcs[0]}', y=f'PC{pcs[1]}'), use_container_width=True)
    elif len(pcs) == 3:
        st.plotly_chart(px.scatter_3d(principal_df,x=f'PC{pcs[0]}', y=f'PC{pcs[1]}', z=f'PC{pcs[2]}'), use_container_width=True)



