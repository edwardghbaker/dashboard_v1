#%%
import streamlit_authenticator as stauth


#%%

stauth.Hasher(['abc', 'def']).generate()
