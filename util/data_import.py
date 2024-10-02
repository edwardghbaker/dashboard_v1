# %% Imports 
import pandas as pd 
import numpy as np 
from tqdm import tqdm

import utm

#%% Define functions

def data_to_pkl(data_file, df_out=False):
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
    data['Date'] = [df[df['SAMPLEID']==i]['SAMPLEDATE'].iloc[0] for i in data.index]
    data['Date'] = pd.to_datetime(data['Date'],yearfirst=True)
    data['SITE ID'] = [df[df['SAMPLEID']==i]['NAME'].iloc[0] for i in data.index]
    if df_out:
        return data
    else:
        data.to_pickle(data_file.replace('.xls', '.pkl'))

def locations_to_pkl(loc_file: str,
                     data_files: list):
    df = pd.read_excel(loc_file,header=1)
    df[['UTM Easting','UTM Northing']] = df[['UTM Easting','UTM Northing']].map(lambda x: float(x.replace('E', '').replace('N','')))
    df = df[df['UTM Easting'] != 0]
    df = df.dropna(subset='Zone')
    df['lat'] = [utm.to_latlon(i,j,19,'J')[0] for i,j in zip(df['UTM Easting'],df['UTM Northing'])]
    df['lon'] = [utm.to_latlon(i,j,19,'J')[1] for i,j in zip(df['UTM Easting'],df['UTM Northing'])]
    df['Last Sample'] = pd.to_datetime(df['Last Sample'])
    wq_dfs = []
    for data_file in data_files:
        wq = data_to_pkl(data_file,df_out=True)
        cols = wq.select_dtypes(include=['number','datetime']).columns # type: ignore
        df[cols] = np.nan
        wq = wq.sort_values('Date',ascending=False) # type: ignore
        wq_dfs.append(wq)
    
    for wq in wq_dfs:
        for i in tqdm(range(len(df))):
            for c in df.columns[14:]:
                try:
                    df.loc[i,c] = wq[wq['SITE ID']==df.loc[i,'Name']][c].iloc[0]
                except:
                    pass

    df.to_pickle(loc_file.replace('.xlsx','.pkl'))


# %%

if __name__ == '__main__':
    import os

    gwq = os.getcwd().split('dashboard_v1')[0]+'dashboard_v1\\data\\gwq.xls'
    swq = os.getcwd().split('dashboard_v1')[0]+'dashboard_v1\\data\\swq.xls'

    data_to_pkl(gwq)
    data_to_pkl(swq)

    location_data = os.getcwd().split('dashboard_v1')[0]+'dashboard_v1\\data\\locations.xlsx'

    locations_to_pkl(location_data,
                     data_files=[gwq,swq])
    
# %%
