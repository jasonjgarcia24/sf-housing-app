import os
import math
import hvplot.pandas

import numpy  as np
import pandas as pd
import panel  as pn
from ipywidgets import interact, interactive_output

from housing.mashvisor_client  import MashvisorNeighborhoodParser
from housing.mashvisor_config  import get_label
from utils.plotting.hvplot     import scatter, widgets


mash = MashvisorNeighborhoodParser()

xdata = "name"
ydata = ["one_room_value", "two_room_value", "three_room_value", "four_room_value"]
cdata = "price_per_sqft"
sdata = "traditional_rental.roi"

xlabel, *ylabel, clabel = [get_label(data, mash.scales(data)["text"]) for data in [xdata] + ydata + [cdata]]
title  = f"Average Value (y) by Neighborhood (x) vs<br>{get_label(cdata)} (c) vs {get_label(sdata)} (s)"

df_labels  = [get_label(col) for col in mash.df.columns]
parameters = widgets.parameter_widgets(xdata, ydata, cdata, sdata, df_labels)

parameters["children"]["xaxis"]["dropdown"].observe(scatter.quad)
interact(scatter.quad, x=parameters["children"]["xaxis"]["dropdown"])
