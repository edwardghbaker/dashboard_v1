import streamlit as st
import streamlit_authenticator as stauth

import numpy as np
import pandas as pd
import plotly.express as px

import yaml
with open('user_details.yaml') as file:
    config = yaml.load(file, Loader=yaml.loader.SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)
name, authentication_status, username = authenticator.login('main')

if authentication_status:
    authenticator.logout('main')
    st.write(f'Welcome *{name}*')
    st.title('Some content')
elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')

pg = st.navigation([st.Page("sections\map.py",title='Map'), st.Page("sections\graphing.py",title='Graph'), st.Page("sections\PCA.py",title='PCA')])
pg.run()