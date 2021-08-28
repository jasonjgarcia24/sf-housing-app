import sys
sys.path.append(".")

import pandas as pd

from pathlib import Path


FIND_COLS_FUNC = lambda df, sub: [col for col in df.columns if sub in col]
NORMALIZE_FUNC = lambda df, col: (df[col] - df[col].mean()) / df[col].std()
POS_SLIDE_FUNC = lambda df, col: df[col] + abs(df[col]) if df[col].min() < 0 or df[col].std() != 0.0 else df[col]


def get_neighborhood_df():
    historical_neighborhood_df = pd.read_csv(Path("./data/historical-neighborhood-performance_data.csv"))
    list_neighborhood_df       = pd.read_csv(Path("./data/list-neighborhood_data.csv"))
    top_neighborhood_df        = pd.read_csv(Path("./data/top-neighborhood_data.csv"))
    overview_neighborhood_df   = pd.read_csv(Path("./data/overview-neighborhood_data.csv"))

    df = historical_neighborhood_df.join(
        list_neighborhood_df.set_index("id"),
        on="id",
        how="left",
        rsuffix=".list_neighborhood"
    )

    df = df.join(
        top_neighborhood_df.set_index("id"),
        on="id",
        how="left",
        rsuffix=".top_neighborhood"
    )

    df = df.join(
        overview_neighborhood_df.set_index("id"),
        on="id",
        how="left",
        rsuffix=".overview_neighborhood"
    )

    df = __remove_duplicate_columns(df)
    df = __clean_date_column_names(df)

    return df


def group_df(df, sort_col):
    val_cols     = ["zero_room_value", "one_room_value", "two_room_value", "three_room_value", "four_room_value"]
    avg_val_cols = ["averages.one_room_value", "averages.two_room_value",
                    "averages.three_room_value", "averages.four_room_value",
                    "airbnb_rental.rental_income"]

    for col in val_cols + avg_val_cols:
        df[col] = df[col].apply(float)
        
    df_by = df.groupby(sort_col).mean()

    for col in val_cols + avg_val_cols:
        df_by[col] = df_by[col].apply(lambda x: x / 1000)

    df_by["price_per_sqft"] = df_by["price_per_sqft"].apply(lambda x: x / 100)
    df_by["median_price"]   = df_by["median_price"].apply(lambda x: x / 100000)
    df_by["walkscore"]      = NORMALIZE_FUNC(df_by, "walkscore")
    df_by["walkscore"]      = POS_SLIDE_FUNC(df_by, "walkscore")

    return df_by, val_cols, avg_val_cols


def __remove_duplicate_columns(df):
    for sub in [".list_neighborhood", ".top_neighborhood", ".overview_neighborhood"]:
        df.drop(columns=FIND_COLS_FUNC(df, sub), inplace=True)
        
    df.drop(columns=[
        'investment_rentals.airbnb_rental.roi',
        'investment_rentals.airbnb_rental.cap_rate',
        'investment_rentals.airbnb_rental.rental_income',
        'investment_rentals.traditional_rental.roi',
        'investment_rentals.traditional_rental.cap_rate',
        'investment_rentals.traditional_rental.rental_income',
    ], inplace=True)

    return df


def __clean_date_column_names(df):
    months_cols     = FIND_COLS_FUNC(df, "months")
    new_months_cols = {col: col.replace("months.", "") for col in months_cols}

    df.rename(columns=new_months_cols, inplace=True)

    return df

