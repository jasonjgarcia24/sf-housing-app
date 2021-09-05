import pandas as pd

from utils  import frange


def get_ticks(ds: pd.Series):    
    tickvals = [ds.min(), ds.max()]
    tickstep = (tickvals[-1]-tickvals[0]) / 5
    tickvals = list(frange(*tickvals, tickstep)) + [tickvals[-1]]

    return tickvals

