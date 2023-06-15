import pandas as pd
import streamlit as st
from bokeh.plotting import figure
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.models import CategoricalColorMapper
from bokeh.palettes import Spectral6

# Load data
data = pd.read_csv("/app/finalproject_visdat/TUBES_VISDAT/finalproject_topscore.csv")
data.set_index('Year', inplace=True)

# Make a list of the unique values from the region column: regions_list
league_list = data.League.unique().tolist()

# Make a color mapper: color_mapper
color_mapper = CategoricalColorMapper(factors=league_list, palette=Spectral6)

# Create the figure: plot
plot = figure(title='2016', x_axis_label='Minutes Played', y_axis_label='Goal Scored',
        plot_height=400, plot_width=700, tools=[HoverTool(tooltips='@PlayerName')])

# Create the ColumnDataSource: source
source = ColumnDataSource(data={
    'x': data.loc[2016].Mins,
    'y': data.loc[2016].Goals,
    'Shots': data.loc[2016].Shots,
    'OnTarget': data.loc[2016].OnTarget,
    'League': data.loc[2016].League,
    'PlayerName': data.loc[2016].PlayerName,
})

# Add a circle glyph to the figure plot
plot.circle(x='x', y='y', source=source, fill_alpha=0.8,
            color=dict(field='League', transform=color_mapper), legend='League')

# Set the legend and axis attributes
plot.legend.location = 'bottom_left'


def update_plot(year, x_axis, y_axis):
    # Update the data source based on the selected year, x-axis, and y-axis
    new_data = {
        'x': data.loc[year][x_axis],
        'y': data.loc[year][y_axis],
        'Shots': data.loc[year].Shots,
        'OnTarget': data.loc[year].OnTarget,
        'League': data.loc[year].League,
        'PlayerName': data.loc[year].PlayerName,
    }
    source.data = new_data

    # Update plot title, x-axis label, and y-axis label
    plot.title.text = f'TOPSCORE BY FARHAN & REINALDY {year}'
    plot.xaxis.axis_label = x_axis
    plot.yaxis.axis_label = y_axis


# Create Streamlit widgets
year = st.slider('Year', min_value=2016, max_value=2019, step=1, value=2016)
x_axis = st.selectbox('x-axis data', options=['Mins', 'Goals', 'Shots', 'OnTarget'], index=0)
y_axis = st.selectbox('y-axis data', options=['Mins', 'Goals', 'Shots', 'OnTarget'], index=0)

# Update the plot based on the widget values
update_plot(year, x_axis, y_axis)

# Display the plot using Streamlit
st.bokeh_chart(plot)
