import yaml
import streamlit as st
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
from streamlit_authenticator.utilities import LoginError

from util.add_logo import add_logo

st.set_page_config(layout='wide')


with open('user_details.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Pre-hashing all plain text passwords once
# Hasher.hash_passwords(config['credentials'])

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# Creating a login widget
try:
    authenticator.login(location='sidebar',key='Login')
except LoginError as e:
    st.error(e)

if st.session_state["authentication_status"]:
    authenticator.logout()
    st.write('___')
    st.sidebar.image(add_logo(logo_path=r"KP_stuff\KP-FullLogo-Colour-RGB.png")) 

    pg = st.navigation([st.Page(r"sections\home.py",title='Home'),
                        st.Page(r"sections\map.py",title='Map'),
                        st.Page(r"sections\graphing.py",title='Graph'),
                        st.Page(r"sections\PCA.py",title='PCA')])
    
    st.sidebar.markdown("Knight Piesold's Data Explorer")
    st.sidebar.markdown("Edward Baker")
    pg.run()
elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')

