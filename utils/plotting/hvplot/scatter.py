import pandas as pd


def quad(
        df: pd.DataFrame, x: str, y: list, c: str, s: str,
        xlabel=None, ylabel=None, clabel=None, title="Quad Scatter",
        hover_cols=[], height=450, width=450, rot=45, scale=20,
    ):
    def single(_y, _ylabel):
        trace = df.hvplot.scatter(
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

        return trace
    
    fig = (
        single(y[0], ylabel[0]) + \
        single(y[1], ylabel[1]) + \
        single(y[2], ylabel[2]) + \
        single(y[3], ylabel[3])
    ).opts(
        title=title,
    ).cols(2)

    return fig
