import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px


pg = st.navigation([st.Page("sections\map.py",title='Kill me'), st.Page("sections\graphing.py"), st.Page("sections\PCA.py")])
pg.run()