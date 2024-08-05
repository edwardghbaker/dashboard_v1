import streamlit as st

pg = st.navigation([st.Page("pages\map.py",title='Kill me',), st.Page("pages\graphing.py"), st.Page("pages\PCA.py")])
pg.run()