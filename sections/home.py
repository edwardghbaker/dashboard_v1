
import streamlit as st
#st.set_page_config(layout="wide")

import numpy as np
import pandas as pd
import plotly.express as px



col1, col2 = st.columns([1,3])
col1.image(r'data\Lundin_Logo.png')
col1.image(r'KP_stuff\KP-FullLogo-Colour-RGB.png')
col2.image(r'data\josemaria-copper-gold-silver-project.jpg')

st.write('This is the home page of the Knight Piesold Data Explorer. Use the sidebar to navigate to the different sections of the app.')

st.write('The Josemaria Project is located in the high-altitude Andean Cordillera between the Atacama Region of Chile and the San Juan and La Rioja provinces of Argentina. The Project consists of a conventional open pit with an ore processing facility processing mill feed at a nominal rate of 175,000 tonnes per day (tpd). A total of almost 1600 Mt of ore is planned for processing over the 25 year mine life, which will produce over 1570 Mt of tailings solids. ')

st.write('Some other crap about the project')