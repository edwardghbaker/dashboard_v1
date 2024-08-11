# %% Imports 
import pandas as pd 
import numpy as np 
from tqdm import tqdm

import utm

#%% Define functions

def data_to_pkl(data_file):
    def arr_to_nan(x):
        if type(x) == np.ndarray:
            return np.nan
        else:
            try:
                return float(x)
            except:
                return np.nan

    df = pd.read_excel(data_file, sheet_name='Results')

    data = df.pivot_table(index='SAMPLEID', columns='ANALYTE', values='CONCENTRATION')

    data = data.map(pd.to_numeric)
    data = data.map(arr_to_nan)

    data.to_pickle(data_file.replace('.xls', '.pkl'))


def location_to_pkl(data_file):

    return NotImplemented


#%%

def locations_to_pkl(loc_file):
    df = pd.read_excel(r'..\data\locations.xlsx',header=1)
    df[['UTM Easting','UTM Northing']] = df[['UTM Easting','UTM Northing']].map(lambda x: float(x.replace('E', '').replace('N','')))
    df = df[df['UTM Easting'] != 0]
    df = df.dropna(subset='Zone')
    df['lat'] = [utm.to_latlon(i,j,19,'J')[0] for i,j in zip(df['UTM Easting'],df['UTM Northing'])]
    df['lon'] = [utm.to_latlon(i,j,19,'J')[1] for i,j in zip(df['UTM Easting'],df['UTM Northing'])]
    df.to_pickle(loc_file.replace('.xlsx', '.pkl'))
# %%

if __name__ == '__main__':
    gwq = r'C:\Users\User\Documents\GitHub\dashboard_v1\data\gwq.xls'
    swq = r'C:\Users\User\Documents\GitHub\dashboard_v1\data\swq.xls'
    data_to_pkl(gwq)
    data_to_pkl(swq)
    location_data = r'..\data\locations.xlsx'
    locations_to_pkl(location_data)
    
# %%
