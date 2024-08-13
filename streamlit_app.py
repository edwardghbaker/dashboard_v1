import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px


pg = st.navigation([st.Page("sections\map.py",title='Map'), st.Page("sections\graphing.py",title='Graph'), st.Page("sections\PCA.py",title='PCA')])
pg.run()