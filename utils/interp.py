import pandas as pd
import numpy  as np


# Find gross rent and sale price/square foot rates of increase
def interpolate(df, col, freq):
    if isinstance(df, pd.Series): return df[col]
    
    df       = df.set_index("year")
    df.index = pd.to_datetime(df.index, format="%Y")
    df       = df.resample(freq).sum()

    df.loc[df[col]==0, col] = np.nan
    
    return df.interpolate(method='linear')[col]

def interpolate_1Y(df):
    neighborhood_grouped_df = df.groupby(["neighborhood", "year"]).mean().sort_index()
    neighborhood_grouped_df = neighborhood_grouped_df.reset_index(level=[1])
    neighborhoods           = list(neighborhood_grouped_df.index.unique())

    func = lambda x: x.pct_change().dropna().mean() * 100 if len(x.dropna()) > 1 else None

    neighborhood        = []
    gross_rent          = []
    sale_price_sqr_foot = []

    for n in neighborhoods:
        neighborhood.append(n)
        gross_rent_ds          = interpolate(neighborhood_grouped_df.loc[n], "gross_rent", "Y")
        sale_price_sqr_foot_ds = interpolate(neighborhood_grouped_df.loc[n], "sale_price_sqr_foot", "Y")
    
    
        if isinstance(gross_rent_ds, pd.Series):
            gross_rent.append(func(gross_rent_ds))
            sale_price_sqr_foot.append(func(sale_price_sqr_foot_ds))
        else:
            gross_rent.append(None)
            sale_price_sqr_foot.append(None)

        
    neighborhood_rate_df = pd.DataFrame({"Neighborhood":        neighborhood,
                                         "gross_rent":          gross_rent,
                                         "sale_price_sqr_foot": sale_price_sqr_foot})

    return neighborhood_rate_df

