import hvplot.pandas


DEFAULT_Y      = ["one_room_value", "two_room_value", "three_room_value", "four_room_value"]
DEFAULT_YLABEL = ["One Room Value (Thousands)", "Two Room Value (Thousands)", "Three Room Value (Thousands)", "Four Room Value (Thousands)"]

def scatter_per_neighborhood(df,y=DEFAULT_Y, c="price_per_sqft", s="traditional_rental.roi",
                             ylabel=DEFAULT_YLABEL, clabel="Price/SqFt", title="Average Value by Neighborhood"):

    ylim = lambda df, cols, buff: [0, (df[cols]).sum(axis=1).max()+buff]
    hover_cols = ["mashMeter", ]

    xlabel="Neighborhood"
    height = 450
    width  = 450
    
    fig = (df.hvplot.scatter(
        x="name",
        y=y[0],
        c=c,
        s=s,
        xlabel=xlabel,
        ylabel=ylabel[0],
        clabel=clabel,
        scale=20,
        rot=45,
        height=height,
        width=width,
    ) + \
    df.hvplot.scatter(
        x="name",
        y=y[1],
        c=c,
        s=s,
        xlabel=xlabel,
        ylabel=ylabel[1],
        clabel=clabel,
        scale=20,
        rot=45,
        height=height,
        width=width,
    ) + \
    df.hvplot.scatter(
        x="name",
        y=y[2],
        c=c,
        s=s,
        xlabel=xlabel,
        ylabel=ylabel[2],
        clabel=clabel,
        scale=20,
        rot=45,
        height=height,
        width=width,
    ) + \
    df.hvplot.scatter(
        x="name",
        y=y[3],
        c=c,
        s=s,
        xlabel=xlabel,
        ylabel=ylabel[3],
        clabel=clabel,
        scale=20,
        rot=45,
        height=height,
        width=width,
    )
    ).opts(
        title=title,
    ).cols(2)

    return fig

