import hvplot.pandas

import pandas as pd

from utils.config.mashvisor_labels import get_label


def quad_scatter(
        df: pd.DataFrame, x: str, y: list, c: str, s: str,
        xlabel=None, ylabel=None, clabel=None, title="Quad Scatter",
        hover_cols=[], height=450, width=450, rot=45, scale=20,
    ):

    if not xlabel:
        xlabel = get_label(x)

    if not ylabel:
        ylabel = [get_label(_y) for _y in y]

    if not clabel: 
        clabel = get_label(c)

    def single_scatter(_y, _ylabel):
        _fig = df.hvplot.scatter(
            x=x,
            y=_y,
            c=c,
            s=s,
            xlabel=xlabel,
            ylabel=_ylabel,
            clabel=clabel,
            scale=scale,
            rot=rot,
            height=height,
            width=width,
        )

        return _fig
    
    fig = (
        single_scatter(y[0], ylabel[0]) + \
        single_scatter(y[1], ylabel[1]) + \
        single_scatter(y[2], ylabel[2]) + \
        single_scatter(y[3], ylabel[3])
    ).opts(
        title=title,
    ).cols(2)

    return fig

