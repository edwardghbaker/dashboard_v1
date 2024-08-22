#%%
import geopandas as gpd
from shapely import force_2d

GA = gpd.read_file(r'..\data\GA.geojson')
GA = GA.to_crs(epsg=4326)

GA['geometry'] = force_2d(GA['geometry'])

GA.to_file(r'..\data\GA_2d.json')
# %%
