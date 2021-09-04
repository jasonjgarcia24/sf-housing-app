import os
import math

import numpy  as np
import pandas as pd
import plotly.graph_objects as go

from utils  import frange
from utils  import pd_compare
from dotenv import load_dotenv

from housing.mashvisor_config import get_label
from housing.mashvisor_client import MashvisorNeighborhoodParser


def pvr(mash: MashvisorNeighborhoodParser):
    ''' Price vs ROI Scatter Map'''

    # Set the colorbar ticks and custom data for the scatter mapbox
    colorbar_title = f"{get_label('traditional_rental.roi', unit=mash.scales('traditional_rental.roi')['text'], width=15)}"
    tickvals       = get_colorbar_ticks(mash.df)
    customdata, hovertemplate = get_hover_data(mash)

    # Set the size parameters for the scatter mapbox
    size      = mash.df["price_per_sqft"] / mash.scales("price_per_sqft")["value"]
    sizescale = 10 ** (int(math.log(size.max(), 10)) - 1)

    # Organize the data points for the scatter mapbox
    fig = go.Figure()

    x_values = mash.df["latitude"]
    y_values = mash.df["longitude"]
    s_values = size / sizescale
    c_values = mash.df["traditional_rental.roi"]

    # Add the scattermapbox trace to the figure
    fig.add_scattermapbox(
        lat=x_values,
        lon=y_values,
        mode="markers",
        marker=go.scattermapbox.Marker(
            size=s_values,
            color=c_values,
            colorbar=dict(
                title=colorbar_title,
                thickness=20,
                tickvals=tickvals,
                outlinewidth=0,
                tickformat=".2f",
            ),
        ),
        customdata=customdata,
        hovertemplate=hovertemplate,
    )

    # Customize the figure layout
    fig.update_layout(
        title="<b>Price/Sqaure Foot and Traditional Rental ROI</b><br>Chicago",
        width=900,
        height=750,
        mapbox=dict(
            accesstoken=get_mapbox_api_token(),
            zoom=12,
            center=dict(
                lat=center_loc(mash.df["latitude"]),
                lon=center_loc(mash.df["longitude"]),
            ),
        ),
        margin=go.layout.Margin(
            l=45,
            r=150,
            b=50,
            t=100,
            pad=4
        ),
    )

    return fig


def get_mapbox_api_token():
    load_dotenv()
    return os.getenv("mapbox_api_access_token".upper())


def get_colorbar_ticks(df: pd.DataFrame):    
    tickvals = [df["traditional_rental.roi"].min(), df["traditional_rental.roi"].max()]
    tickstep = (tickvals[-1]-tickvals[0]) / 5
    tickvals = list(frange(*tickvals, tickstep)) + [tickvals[-1]]

    return tickvals


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
    Location : (%{{lat:.2f}}, %{{lon:.2f}})<br><br>
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

