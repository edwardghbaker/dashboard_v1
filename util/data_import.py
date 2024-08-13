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

def locations_to_pkl(loc_file):
    df = pd.read_excel(loc_file,header=1)
    df[['UTM Easting','UTM Northing']] = df[['UTM Easting','UTM Northing']].map(lambda x: float(x.replace('E', '').replace('N','')))
    df = df[df['UTM Easting'] != 0]
    df = df.dropna(subset='Zone')
    df['lat'] = [utm.to_latlon(i,j,19,'J')[0] for i,j in zip(df['UTM Easting'],df['UTM Northing'])]
    df['lon'] = [utm.to_latlon(i,j,19,'J')[1] for i,j in zip(df['UTM Easting'],df['UTM Northing'])]
    df.to_pickle(loc_file.replace('.xlsx', '.pkl'))


# %%

# if __name__ == '__main__':
#     gwq = r'C:\Users\User\Documents\GitHub\dashboard_v1\data\gwq.xls'
#     swq = r'C:\Users\User\Documents\GitHub\dashboard_v1\data\swq.xls'
#     data_to_pkl(gwq)
#     data_to_pkl(swq)
#     location_data = r'..\data\locations.xlsx'
#     locations_to_pkl(location_data)
    
# %%
loc_file = r'..\data\locations.xlsx'
df = pd.read_excel(r'..\data\locations.xlsx',header=1)
df[['UTM Easting','UTM Northing']] = df[['UTM Easting','UTM Northing']].map(lambda x: float(x.replace('E', '').replace('N','')))
df = df[df['UTM Easting'] != 0]
df = df.dropna(subset='Zone')
df['lat'] = [utm.to_latlon(i,j,19,'J')[0] for i,j in zip(df['UTM Easting'],df['UTM Northing'])]
df['lon'] = [utm.to_latlon(i,j,19,'J')[1] for i,j in zip(df['UTM Easting'],df['UTM Northing'])]
#df.to_pickle(loc_file.replace('.xlsx', '.pkl'))
data_file =  r'C:\Users\User\Documents\GitHub\dashboard_v1\data\swq.xls'
swq = data_to_pkl(data_file,df_out=True)
cols = swq.select_dtypes(include=['number','datetime']).columns
df[cols] = np.nan

for i in df.index:
    n = df.loc[i,'Name']

    for j in cols:
        swq1 = swq[swq['SITE ID']==n].sort_values('Date')[j].dropna()
        try:
            if j == 'Date':
                df.loc[i,j] = df.loc[i,j].astype('datetime64[ns]')
            df.loc[i,j] = swq1.iloc[-1]
        except:
            continue    



#     swq2 = swq1.select_dtypes(include=['number','datetime']).columns
#     print(swq1)
# # %%

# %%
