import numbers

import plotly.graph_objects as go

from ipywidgets import (
    Button,
    Dropdown,
    GridBox,
    HTML,
    ButtonStyle,
    Layout,
)

from utils.plotting.colorbar  import get_ticks
from housing.mashvisor_config import get_label
from housing.mashvisor_client import MashvisorNeighborhoodParser


def __label_widget(title, fontcolor="white", fontfamily="arial", fontvariant="small-caps", fontsize="150%"):
    label = HTML(
        value=f"""
        <font color={fontcolor} 
        style='font-family:{fontfamily}; 
        font-variant:{fontvariant}; 
        font-size:{fontsize}'>{title}:
        """,
        layout=Layout(width="auto", grid_area="header"),
        style=dict(font_weight="bold"),
    )
    
    return label


def __dropdown_widget(cols, val, width="200px", gridarea="main"):
    dropdown =  Dropdown(
        options=cols,
        value=val,
        disabled=False,
        layout=Layout(width=width, grid_area=gridarea),
    )

    # interactive_output(scatter.quad, controls={gridarea: dropdown})
    
    return dropdown


def __button_widget(description, tooltip="", gridarea="main", buttoncolor="white"):
    button = Button(
        description=description,
        disabled=False,
        button_style='',
        tooltip=tooltip,
        layout=Layout(width="75px", grid_area=gridarea),
        style=ButtonStyle(button_color=buttoncolor),
    )
    
    return button


def __single_dropdown_grid(children,
                         width="210px",
                         margin="0px",
                         padding="0px",
                         gridarea_label="header",
                         gridarea_dropdown="main",
                         gridarea_button="sidebar",
                         gridarea="axis"):
    grid = GridBox(
        children=children,
        layout=Layout(
            width=width,
            margin=margin,
            padding=padding,
            grid_gap="0px",
            grid_template_columns="100%",
            grid_template_rows="auto auto auto",
            grid_template_areas=f"""
            '{gridarea_label}'
            '{gridarea_dropdown}'
            '{gridarea_button}'
            """,
            border="solid 3px orange",
            grid_area=gridarea,
        ))
    
    return grid
    

def dynamic_4d(
    plt: go.FigureWidget, mash: MashvisorNeighborhoodParser,
    xdata: list, ydata: list, cdata: list, sdata: list, labels: list
    ):    

    yaxis, xaxis, caxis, saxis, parent = {}, {}, {}, {}, {}

    yaxis["label"] = __label_widget("Y-Axis Settings")
    xaxis["label"] = __label_widget("X-Axis Settings")
    caxis["label"] = __label_widget("C-Value Settings")
    saxis["label"] = __label_widget("S-Value Settings")

    yaxis["button"] = __button_widget("Restore",
                                    tooltip="Restore to default y-axis settings.",
                                    gridarea="y_sidebar",
                                    buttoncolor="skyblue")
    xaxis["button"] = __button_widget("Restore",
                                    tooltip="Restore to default x-axis settings.",
                                    gridarea="x_sidebar",
                                    buttoncolor="skyblue")
    caxis["button"] = __button_widget("Restore",
                                    tooltip="Restore to default color settings.",
                                    gridarea="c_sidebar",
                                    buttoncolor="skyblue")
    saxis["button"] = __button_widget("Restore",
                                    tooltip="Restore to default size settings.",
                                    gridarea="s_sidebar",
                                    buttoncolor="skyblue")

    yaxis["dropdown"] = []
    yaxis["dropdown"].append(__dropdown_widget(labels, get_label(ydata[0]), gridarea="y_r1c1"))
    yaxis["dropdown"].append(__dropdown_widget(labels, get_label(ydata[1]), gridarea="y_r1c2"))
    yaxis["dropdown"].append(__dropdown_widget(labels, get_label(ydata[2]), gridarea="y_r2c1"))
    yaxis["dropdown"].append(__dropdown_widget(labels, get_label(ydata[3]), gridarea="y_r2c2"))

    xaxis["dropdown"] = __dropdown_widget([get_label(xdata)] + labels, get_label(xdata), gridarea="x_r1c1")
    caxis["dropdown"] = __dropdown_widget(labels, get_label(cdata)                     , gridarea="c_r1c1")
    saxis["dropdown"] = __dropdown_widget(labels, get_label(sdata)                     , gridarea="s_r1c1")

    yaxis["grid"] = GridBox(
        children=[
            yaxis["label"],
            *yaxis["dropdown"],
            yaxis["button"],
            ],
        layout=Layout(
            width="422px",
            justify_content="space-around",
            margin="0px",
            padding="0px",
            grid_gap="0px 0px 0px",
            grid_template_columns="25% 25% 25% 25%",
            grid_template_rows="auto auto auto auto",
            grid_template_areas="""
            'header header header .'
            'y_r1c1 . y_r1c2 .'
            'y_r2c1 . y_r2c2 .'
            'y_sidebar . . .'
            """,
            border="solid 3px orange",
            grid_area="y_axis",
        ))

    xaxis_gridarea = {
        "gridarea_label":    "header",
        "gridarea_dropdown": "x_r1c1",
        "gridarea_button":   "x_sidebar",
        "gridarea":          "x_axis"
        }
    caxis_gridarea = {
        "gridarea_label":    "header",
        "gridarea_dropdown": "c_r1c1",
        "gridarea_button":   "c_sidebar",
        "gridarea":          "c_axis"
        }
    saxis_gridarea = {
        "gridarea_label":    "header",
        "gridarea_dropdown": "s_r1c1",
        "gridarea_button":   "s_sidebar",
        "gridarea":          "s_axis"
        }

    xaxis_widgets = [xaxis["label"], xaxis["dropdown"], xaxis["button"]]
    caxis_widgets = [caxis["label"], caxis["dropdown"], caxis["button"]]
    saxis_widgets = [saxis["label"], saxis["dropdown"], saxis["button"]]

    xaxis["grid"] = __single_dropdown_grid(xaxis_widgets, width="422px", **xaxis_gridarea)
    caxis["grid"] = __single_dropdown_grid(caxis_widgets, width="210px", **caxis_gridarea)
    saxis["grid"] = __single_dropdown_grid(saxis_widgets, width="210px", **saxis_gridarea)

    parent["grid"] = GridBox([
        yaxis["grid"],
        xaxis["grid"],
        caxis["grid"],
        saxis["grid"],
    ],
    layout=Layout(
        width="950px",
        justify_content="flex-start",
        margin="0px",
        padding="0px",
        grid_gap="2px",
        grid_template_columns="210px 210px 420px",
        grid_template_rows="auto auto auto",
        grid_template_areas="""
        'y_axis yaxis .'
        'x_axis x_axis .'
        'c_axis s_axis .'
        """
    ))

    parent["children"] = {}
    parent["children"]["xaxis"] = xaxis
    parent["children"]["yaxis"] = yaxis
    parent["children"]["caxis"] = caxis
    parent["children"]["saxis"] = saxis
    
    def cdropdown_callback(change):        
        xdata = get_label(xaxis["dropdown"].value, return_type="key")
        sdata = get_label(saxis["dropdown"].value, return_type="key")
        cdata = get_label(change.new, return_type="key")
        title = title=f"<b>{get_label(cdata)} (c) and {get_label(sdata)} (s)</b><br>by {get_label(xdata)} (x)"
        
        c_values       = mash.df[cdata]
        colorbar_title = f"{get_label(cdata, unit=mash.scales(cdata)['text'], width=15)}"
        tickvals       = get_ticks(mash.df[cdata])
        
        with plt.batch_update():
            for i in range(4):
                plt.layout.title.text    = title
                plt.data[i].marker.color = c_values
                
                if i == 3:
                    plt.data[i].marker.colorbar.title    = colorbar_title
                    plt.data[i].marker.colorbar.tickvals = tickvals
    
    def sdropdown_callback(change):    
        xdata = get_label(xaxis["dropdown"].value, return_type="key")
        cdata = get_label(caxis["dropdown"].value, return_type="key")
        sdata = get_label(change.new, return_type="key")
        title = title=f"<b>{get_label(cdata)} (c) and {get_label(sdata)} (s)</b><br>by {get_label(xdata)} (x)"
        
        s_values  = mash.base(sdata)
        
        with plt.batch_update():
            for i in range(4):
                plt.layout.title.text   = title
                plt.data[i].marker.size = s_values
    
    def xdropdown_callback(change):
        xdata = get_label(change.new, return_type="key")
        cdata = get_label(caxis["dropdown"].value, return_type="key")
        sdata = get_label(saxis["dropdown"].value, return_type="key")
        title = title=f"<b>{get_label(cdata)} (c) and {get_label(sdata)} (s)</b><br>by {get_label(xdata)} (x)"
        
        x_values = mash.df.index if xdata == mash.df.index.name else mash.df[xdata]
        
        with plt.batch_update():
            for i in range(4):
                plt.layout.title.text = title
                plt.data[i].x         = x_values
                
                idx    = str(i+1) if i > 0 else ""
                xtitle = get_label(xdata, unit=mash.scales(xdata)['text'], width=35)
                plt.layout[f"xaxis{idx}"].title     = xtitle if i > 1 else ""
                plt.layout[f"xaxis{idx}"].tickangle = 0 if isinstance(x_values[0], numbers.Number) else 45
    
    def ydropdown_callback(change):
        ydata = get_label(change.new, return_type="key")

        gridarea = change["owner"].layout.grid_area
        y_values = mash.df[ydata]
        
        with plt.batch_update():
            for i, (row, col) in enumerate(zip([1, 1, 2, 2], [1, 2, 1, 2])):
                if f"y_r{row}c{col}" == gridarea:
                    plt.data[i].y = y_values

                    idx    = str(i+1) if i > 0 else ""
                    ytitle = get_label(ydata, unit=mash.scales(ydata)['text'], width=20)
                    plt.layout[f"yaxis{idx}"].title = ytitle
                    break

    def xbutton_restore_callback(change):
        xaxis["dropdown"].value = get_label(xdata)

    def cbutton_restore_callback(change):
        caxis["dropdown"].value = get_label(cdata)

    def sbutton_restore_callback(change):
        saxis["dropdown"].value = get_label(sdata)

    def ybutton_restore_callback(change):
        for i in range(len(ydata)):
            yaxis["dropdown"][i].value = get_label(ydata[i])
                    
    xaxis["dropdown"].observe(xdropdown_callback, names="value")
    caxis["dropdown"].observe(cdropdown_callback, names="value")
    saxis["dropdown"].observe(sdropdown_callback, names="value")
    
    for i in range(len(ydata)):
        yaxis["dropdown"][i].observe(ydropdown_callback, names="value")

    xaxis["button"].on_click(xbutton_restore_callback)
    saxis["button"].on_click(sbutton_restore_callback)
    caxis["button"].on_click(cbutton_restore_callback)
    yaxis["button"].on_click(ybutton_restore_callback)
        
    return parent
    
