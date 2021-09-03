import os
import hvplot.pandas

import pandas as pd
import plotly.graph_objects as go


from dotenv import load_dotenv
from plotly.subplots import make_subplots


def mb_quad_scatter(
        df: pd.DataFrame, x: str, y: list, c: str, s: str,
        xlabel=None, ylabel=None, clabel=None, title="Quad Scatter",
        hover_cols=[], height=450, width=450, rot=45,
    ):

    def single_scatter(_y, _ylabel, row, col):
        trace = go.Scatter(
            mode="markers",
            x=x,
            y=_y,
            marker=dict(
                size=s,
                color=c,
                showscale=True,
            ),
            # row=row,
            # col=col,
            # xlabel=xlabel,
            # ylabel=_ylabel,
            # clabel=clabel,
            # scale=scale,
            # rot=rot ,
            # height=height,
            # width=width,
        )

        return trace
    
    fig = make_subplots(rows=2, cols=2)

    for _y, _ylabel, _r, _c in zip(y, ylabel, [1, 1, 2, 2], [1, 2, 1, 2]):
        fig.add_trace(
            single_scatter(_y, _ylabel, _r, _c),
            row=_r,
            col=_c,
        )

    
    fig.update_layout(
        width=width,
        height=height,
        mapbox=dict(
            accesstoken=get_mapbox_api_token(),
        ),
        margin=go.layout.Margin(
            l=10,
            r=10,
            b=10,
            t=10,
            pad=2
        ),
    )


    # fig = (
    #     single_scatter(y[0], ylabel[0]) + \
    #     single_scatter(y[1], ylabel[1]) + \
    #     single_scatter(y[2], ylabel[2]) + \
    #     single_scatter(y[3], ylabel[3])
    # ).opts(
    #     title=title,
    # ).cols(2)

    return fig


def get_mapbox_api_token():
    load_dotenv()
    return os.getenv("mapbox_api_access_token".upper())


def center_loc(ds: pd.Series):
    return ds.min() + (ds.max() - ds.min()) / 2

