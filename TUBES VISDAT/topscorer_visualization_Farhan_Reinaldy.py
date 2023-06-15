#!/usr/bin/env python
# coding: utf-8

# # <center>Interactive Data Visualization in Python With Bokeh</center>

# ## Adding Interaction

# In[1]:


import pandas as pd
from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.models import CategoricalColorMapper
from bokeh.palettes import Spectral6
from bokeh.layouts import widgetbox, row, gridplot
from bokeh.models import Slider, Select


# In[2]:


data = pd.read_csv("finalproject_topscore.csv")
data.set_index('Year', inplace=True)


# In[3]:


# Make a list of the unique values from the region column: regions_list
League_list = data.League.unique().tolist()

# Make a color mapper: color_mapper
color_mapper = CategoricalColorMapper(factors=League_list, palette=Spectral6)


# In[4]:


# Make the ColumnDataSource: source
source = ColumnDataSource(data={
    'x'           : data.loc[2016].Mins,
    'y'           : data.loc[2016].Goals,
    'Shots'       : data.loc[2016].Shots,
    'OnTarget'    : data.loc[2016].OnTarget,
    'League'      : data.loc[2016].League,
    'PlayerName' : data.loc[2016].PlayerName,
})


# In[ ]:


# Create the figure: plot
plot = figure(title='2016', x_axis_label='Minutes Played', y_axis_label='Goal Scored',
           plot_height=400, plot_width=700, tools=[HoverTool(tooltips='@PlayerName')])

# Add a circle glyph to the figure p
plot.circle(x='x', y='y', source=source, fill_alpha=0.8,
           color=dict(field='League', transform=color_mapper), legend='League')

# Set the legend and axis attributes
plot.legend.location = 'bottom_left'

# Define the callback function: update_plot
def update_plot(attr, old, new):
    # set the `yr` name to `slider.value` and `source.data = new_data`
    yr = slider.value
    x = x_select.value
    y = y_select.value
    # Label axes of plot
    plot.xaxis.axis_label = x
    plot.yaxis.axis_label = y
    # new data
    new_data = {
    'x'             : data.loc[yr][x],
    'y'             : data.loc[yr][y],
    'Shots'         : data.loc[yr].Shots,
    'OnTarget'      : data.loc[yr].OnTarget,
    'League'        : data.loc[yr].League,
    'PlayerName'   : data.loc[yr].PlayerName,
    }
    source.data = new_data
    
    # Add title to figure: plot.title.text
    plot.title.text = 'TOPSCORE BY FARHAN & REINALDY %d' % yr

# Make a slider object: slider
slider = Slider(start=2016, end=2019, step=1, value=2016, title='Year')
slider.on_change('value',update_plot)

# Make dropdown menu for x and y axis
# Create a dropdown Select widget for the x data: x_select
x_select = Select(
    options=['Mins', 'Goals', 'Shots', 'OnTarget'],
    value='Mins',
    title='x-axis data'
)
# Attach the update_plot callback to the 'value' property of x_select
x_select.on_change('value', update_plot)

# Create a dropdown Select widget for the y data: y_select
y_select = Select(
    options=['Mins', 'Goals', 'Shots', 'OnTarget'],
    value='Mins',
    title='x-axis data'
)
# Attach the update_plot callback to the 'value' property of y_select
y_select.on_change('value', update_plot)
    
# Create layout and add to current document
layout = row(widgetbox(slider, x_select, y_select), plot)
curdoc().add_root(layout)


# In[5]:


# bokeh serve --show myapp.py


# For more on all things interaction in Bokeh, [**Adding Interactions**](https://docs.bokeh.org/en/latest/docs/user_guide/interaction.html) in the Bokeh User Guide is a great place to start.

# In[ ]:




