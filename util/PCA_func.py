import pandas as pd

def perform_pca(df,
                components,
                pcs=[1,2,3],
                interpolation='mean',
                scale=True,
                plot=True):
    import pandas as pd
    from sklearn.decomposition import PCA
    from sklearn.preprocessing import StandardScaler
    import plotly.express as px
    """
    Perform Principal Component Analysis (PCA) on the given DataFrame.
    
    Parameters:
        df (pd.DataFrame): The input DataFrame.
        components (list): List of column names to be used as principal components.
        interpolation (str, optional): Interpolation method or None for missing values. Defaults to 'mean'.
    
    Returns:
        pd.DataFrame: DataFrame containing the principal components.
    """
    # Select the columns to be used as principal components
    X = df[components]
    #Only select the columns that are numeric
    X = X.select_dtypes(include=['number'])
    
    if interpolation == 'mean':
        X = X.fillna(X.mean())  # Fill missing values with the mean of the column
    X = X.dropna()  # Drop rows with missing values
    components = X.columns

    ss = StandardScaler().fit(X)

    if scale:
        X = ss.transform(X)

    # Perform PCA
    pca = PCA()
    principal_components = pca.fit_transform(X)
    
    # Create a new DataFrame with the principal components
    principal_df = pd.DataFrame(data=principal_components, columns=['PC{}'.format(i+1) for i in range(len(components))])
    
    # Create a DataFrame with the vectors
    vectors = pd.DataFrame(data=pca.components_, columns=components, index=['PC{}'.format(i+1) for i in range(len(components))])

    # Recreate the original DataFrame
    X_recreated = pca.inverse_transform(principal_components)
    X_recreated = pd.DataFrame(data=X_recreated, columns=components)

    if plot:
        # Plot the explained variance
        fig = px.scatter_3d(principal_df, x=f'PC{pcs[0]}', y=f'PC{pcs[1]}', z=f'PC{pcs[2]}', title='PCA')
        return fig
    
    else:
        return principal_df, vectors, X_recreated

#%%

if __name__ == '__main__':
    # Test the function
    import os
    gwq_file = os.getcwd().split('dashboard_v1')[0]+'dashboard_v1\\data\\gwq.pkl'
    df = pd.read_pickle(gwq_file)
    components = df.select_dtypes(include=['number']).columns[1:]
    perform_pca(df, components).show()
    principal_df, vectors, X_recreated=perform_pca(df, components, plot=False)
    print('Principal components calculated successfully.')

#%%