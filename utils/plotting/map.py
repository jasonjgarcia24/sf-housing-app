import os

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
    tickvals = get_colorbar_ticks(mash.df)
    customdata, hovertemplate = get_hover_data(mash)

    # Organize the data points for the scatter mapbox
    fig = go.Figure()

    fig.add_scattermapbox(
        lat=mash.df["latitude"],
        lon=mash.df["longitude"],
        mode="markers",
        marker=go.scattermapbox.Marker(
            size=mash.df["price_per_sqft"] * 10,
            color=mash.df["traditional_rental.roi"],
            colorbar=dict(
                title=f"{get_label('traditional_rental.roi')}",
                thickness=20,
                tickvals=tickvals,
                outlinewidth=0,
                tickformat=".2f",
                ticksuffix="%",
            ),
        ),
        customdata=customdata,
        hovertemplate=hovertemplate,
    )

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
        
        mash.df["total_listing"]                 / mash.scales("total_listing")["value"],                 #1
        mash.df["airbnb_listings"]               / mash.scales("airbnb_listings")["value"],               #2
        mash.df["num_of_properties"]             / mash.scales("num_of_properties")["value"],             #3
        mash.df["num_of_airbnb_properties"]      / mash.scales("num_of_airbnb_properties")["value"],      #4
        mash.df["num_of_traditional_properties"] / mash.scales("num_of_traditional_properties")["value"], #5
        
        pd_compare.ordinal(mash.df["price_per_sqft"]),         #6
        pd_compare.ordinal(mash.df["traditional_rental.roi"]), #7
        
        mash.df["median_price"]      / mash.scales("median_price")["value"],      #8
        mash.df["zero_room_value"]   / mash.scales("zero_room_value")["value"],   #9
        mash.df["one_room_value"]    / mash.scales("one_room_value")["value"],    #10
        mash.df["two_room_value"]    / mash.scales("two_room_value")["value"],    #11
        mash.df["three_room_value"]  / mash.scales("three_room_value")["value"],  #12
        mash.df["four_room_value"]   / mash.scales("four_room_value")["value"],   #13
        mash.df["single_home_value"] / mash.scales("single_home_value")["value"], #14
        
        pd_compare.ordinal(mash.df["median_price"]),      #15
        pd_compare.ordinal(mash.df["zero_room_value"]),   #16
        pd_compare.ordinal(mash.df["one_room_value"]),    #17
        pd_compare.ordinal(mash.df["two_room_value"]),    #18
        pd_compare.ordinal(mash.df["three_room_value"]),  #19
        pd_compare.ordinal(mash.df["four_room_value"]),   #20
        pd_compare.ordinal(mash.df["single_home_value"]), #21
    ), axis=-1)

    hovertemplate = f"""
    <b>%{{customdata[0]}}</b><br><br>
    Location : (%{{lat:.2f}}, %{{lon:.2f}})<br><br>
    {get_label('total_listing')}  : %{{customdata[1]:d}}<br>
    {get_label('airbnb_listings')} : %{{customdata[2]:d}}<br>
    {get_label('num_of_properties')} : %{{customdata[3]:d}}<br>
    {get_label('num_of_airbnb_properties')} : %{{customdata[4]:d}}<br>
    {get_label('num_of_traditional_properties')} : %{{customdata[5]:d}}<br><br>
    {get_label('price_per_sqft')} : $%{{marker.size:.2f}} (%{{customdata[6]}})<br>
    {get_label('traditional_rental.roi')} : $%{{marker.color:.2f}} (%{{customdata[7]}})<br>
    {get_label('single_home_value')} : $%{{customdata[14]:,.2f}} (%{{customdata[21]}})<br><br>
    {get_label('zero_room_value')} : $%{{customdata[9]:,.2f}} (%{{customdata[16]}})<br>
    {get_label('one_room_value')} : $%{{customdata[10]:,.2f}} (%{{customdata[17]}})<br>
    {get_label('two_room_value')} : $%{{customdata[11]:,.2f}} (%{{customdata[18]}})<br>
    {get_label('three_room_value')} : $%{{customdata[12]:,.2f}} (%{{customdata[19]}})<br>
    {get_label('four_room_value')} : $%{{customdata[13]:,.2f}} (%{{customdata[20]}})
    <extra></extra>
    """

    return customdata, hovertemplate


def center_loc(ds: pd.Series):
    return ds.min() + (ds.max() - ds.min()) / 2

