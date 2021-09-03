import pandas as pd


def get_rank(ds: pd.Series):
    rank = ds.rank(ascending=False).values.astype(int)

    return rank


def ordinal(ds: pd.Series):
    ds = get_rank(ds)
    ordinal = ["%d%s" % (n,"tsnrhtdd"[(n//10%10!=1)*(n%10<4)*n%10::4]) for n in ds]

    return ordinal
