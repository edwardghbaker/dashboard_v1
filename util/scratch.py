#%%
import geopandas as gpd
from glob import glob
from shapely import force_2d
from icecream import ic

# %%

def geojson_to_2d_json(path:str):
    temp = gpd.read_file(path)
    temp = temp.to_crs(epsg=4326)

    temp['geometry'] = force_2d(temp['geometry'])
    new_path = path.replace('.geojson','_2d.json')
    temp.to_file(ic(new_path))

# %%

# for path in glob(r'..\data\*.geojson'):
#     geojson_to_2d_json(path)

#%% Hash passwords
from yaml.loader import SafeLoader
import yaml
import streamlit_authenticator as stauth
from streamlit_authenticator.utilities import Hasher
with open('../user_details.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)
#Pre-hashing all plain text passwords once
Hasher.hash_passwords(config['credentials'])
# %%
