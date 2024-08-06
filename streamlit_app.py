import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px


pg = st.navigation([st.Page("pages\map.py",title='Kill me',), st.Page("pages\graphing.py"), st.Page("pages\PCA.py")])
pg.run()