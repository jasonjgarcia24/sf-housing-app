import os
import math

import numpy  as np
import pandas as pd
import plotly.graph_objects as go

from utils  import frange
from utils  import pd_compare
from dotenv import load_dotenv

from plotly.subplots import make_subplots
from housing.mashvisor_config import get_label
from utils.plotting.colorbar import get_ticks
from housing.mashvisor_client import MashvisorNeighborhoodParser


def quad(mash: MashvisorNeighborhoodParser, x: str, y: list, c: str, s: str):
    ''' Dynamic Scatter Plot '''

    # Identify if x is the index
    xdata = mash.df.index.name if x == mash.df.index.name else x
    
    # Set the colorbar ticks and custom data for the scatter plot
    colorbar_title = f"{get_label(c, unit=mash.scales(c)['text'], width=15)}"
    tickvals       = get_ticks(mash.df[c])
    customdata, hovertemplate = get_hover_data(mash)
    
    # Organize the data points for the scatter plot
    fig = go.FigureWidget(make_subplots(
        rows=2,
        cols=2,
        vertical_spacing=0.06,
        horizontal_spacing=0.12,
        shared_xaxes=True
    ))

    def single_scatter(_x, _y, _r, _c):
        y_values = mash.df[_y]
        x_values = mash.df.index if _x == mash.df.index.name else mash.df[_x]
        s_values = mash.base(s)
        c_values = mash.df[c]

        trace = go.Scatter(
            mode="markers",
            x=x_values,
            y=y_values,
            marker=dict(
                size=s_values,
                color=c_values,
                colorbar=dict(
                    title=colorbar_title,
                    thickness=20,
                    tickvals=tickvals,
                    outlinewidth=0,
                    tickformat=".1f",
                ) if row == col == 2 else dict(),
            ),
            customdata=customdata,
            hovertemplate=hovertemplate,
        )

        return trace

    # Add the scatter plots to its corresponding subplot
    for ydata, row, col in zip(y, [1, 1, 2, 2], [1, 2, 1, 2]):
        fig.add_trace(
            single_scatter(xdata, ydata, row, col),
            row=row,
            col=col,
        )

        # Set the x and y axis labels
        xtitle = get_label(xdata, unit=mash.scales(xdata)['text'], width=35) if row == 2 else ""
        ytitle = get_label(ydata, unit=mash.scales(ydata)['text'], width=35)
        
        fig.update_xaxes(title_text=xtitle, row=row, col=col, tickangle=45)
        fig.update_yaxes(title_text=ytitle, row=row, col=col)
    
    # Customize the figure layout
    fig.update_layout(
        title=f"<b>{get_label(c)} (c) and {get_label(s)} (s)</b><br>by {get_label(x)} (x)",
        width=900,
        height=750,
        mapbox=dict(
            accesstoken=get_mapbox_api_token(),
        ),
        margin=go.layout.Margin(
            l=45,
            r=150,
            b=50,
            t=100,
            pad=4,
        ),
        showlegend=False,
    )
    return fig


def get_mapbox_api_token():
    load_dotenv()
    return os.getenv("mapbox_api_access_token".upper())


def get_hover_data(mash: MashvisorNeighborhoodParser):
    customdata = np.stack((
        mash.df.index, #0

        mash.df["price_per_sqft"]                / mash.scales("price_per_sqft")["value"],                #1
        mash.df["total_listing"]                 / mash.scales("total_listing")["value"],                 #2
        mash.df["airbnb_listings"]               / mash.scales("airbnb_listings")["value"],               #3
        mash.df["num_of_properties"]             / mash.scales("num_of_properties")["value"],             #4
        mash.df["num_of_airbnb_properties"]      / mash.scales("num_of_airbnb_properties")["value"],      #5
        mash.df["num_of_traditional_properties"] / mash.scales("num_of_traditional_properties")["value"], #6
        
        pd_compare.ordinal(mash.df["price_per_sqft"]),                #7
        pd_compare.ordinal(mash.df["total_listing"]),                 #8
        pd_compare.ordinal(mash.df["airbnb_listings"]),               #9
        pd_compare.ordinal(mash.df["num_of_properties"]),             #10
        pd_compare.ordinal(mash.df["num_of_airbnb_properties"]),      #11
        pd_compare.ordinal(mash.df["num_of_traditional_properties"]), #12
        pd_compare.ordinal(mash.df["traditional_rental.roi"]),        #13
    
        mash.df["zero_room_value"]   / mash.scales("zero_room_value")["value"],   #14
        mash.df["one_room_value"]    / mash.scales("one_room_value")["value"],    #15
        mash.df["two_room_value"]    / mash.scales("two_room_value")["value"],    #16
        mash.df["three_room_value"]  / mash.scales("three_room_value")["value"],  #17
        mash.df["four_room_value"]   / mash.scales("four_room_value")["value"],   #18
        mash.df["single_home_value"] / mash.scales("single_home_value")["value"], #19
        
        pd_compare.ordinal(mash.df["zero_room_value"]),   #20
        pd_compare.ordinal(mash.df["one_room_value"]),    #21
        pd_compare.ordinal(mash.df["two_room_value"]),    #22
        pd_compare.ordinal(mash.df["three_room_value"]),  #23
        pd_compare.ordinal(mash.df["four_room_value"]),   #24
        pd_compare.ordinal(mash.df["single_home_value"]), #25
    ), axis=-1)

    hovertemplate = f"""
    <b>%{{customdata[0]}}</b><br><br>
    {get_label('total_listing')} : %{{customdata[2]:d}} (%{{customdata[8]}})<br>
    {get_label('airbnb_listings')} : %{{customdata[3]:d}} (%{{customdata[9]}})<br>
    {get_label('num_of_properties')} : %{{customdata[4]:d}} (%{{customdata[10]}})<br>
    {get_label('num_of_airbnb_properties')} : %{{customdata[5]:d}} (%{{customdata[11]}})<br>
    {get_label('num_of_traditional_properties')} : %{{customdata[6]:d}} (%{{customdata[12]}})<br><br>
    {get_label('price_per_sqft')} : $%{{customdata[1]:.2f}} (%{{customdata[7]}})<br>
    {get_label('traditional_rental.roi')} : $%{{marker.color:.2f}} (%{{customdata[13]}})<br>
    {get_label('single_home_value')} : $%{{customdata[19]:,.2f}} (%{{customdata[25]}})<br><br>
    {get_label('zero_room_value')} : $%{{customdata[14]:,.2f}} (%{{customdata[20]}})<br>
    {get_label('one_room_value')} : $%{{customdata[15]:,.2f}} (%{{customdata[21]}})<br>
    {get_label('two_room_value')} : $%{{customdata[16]:,.2f}} (%{{customdata[22]}})<br>
    {get_label('three_room_value')} : $%{{customdata[17]:,.2f}} (%{{customdata[23]}})<br>
    {get_label('four_room_value')} : $%{{customdata[18]:,.2f}} (%{{customdata[24]}})
    <extra></extra>
    """

    return customdata, hovertemplate


def center_loc(ds: pd.Series):
    return ds.min() + (ds.max() - ds.min()) / 2
