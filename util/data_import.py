# %% Imports 
import pandas as pd 
import numpy as np 
from tqdm import tqdm


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



# %%

if __name__ == '__main__':
    gwq = r'C:\Users\User\Documents\GitHub\dashboard_v1\data\gwq.xls'
    swq = r'C:\Users\User\Documents\GitHub\dashboard_v1\data\swq.xls'
    data_to_pkl(gwq)
    data_to_pkl(swq)


