import argparse
import sys


import datetime as dt

from bokeh.plotting import figure, output_file, save

from bokeh.layouts import row
from bokeh.models import ColumnDataSource
from bokeh.models import DatetimeTickFormatter
from bokeh.models import PrintfTickFormatter
import numpy as np
import pandas as pd

from tracetools_analysis.loading import load_file
from tracetools_analysis.processor.ros2 import Ros2Handler
from tracetools_analysis.utils.ros2 import Ros2DataModelUtil

from numpy import timedelta64



def setup_tracetools():
    # Add paths to tracetools_analysis and tracetools_read.
    # There are two options:
    #   1. from source, assuming a workspace with:
    #       src/tracetools_analysis/
    #       src/ros2/ros2_tracing/tracetools_read/
    sys.path.insert(0, '../')
    sys.path.insert(0, '../../../ros2/ros2_tracing/tracetools_read/')
    #   2. from Debian packages, setting the right ROS 2 distro:
    #ROS_DISTRO = 'rolling'
    #sys.path.insert(0, f'/opt/ros/{ROS_DISTRO}/lib/python3.8/site-packages')

def parse_events_and_evaluate(path, output_path):
    
    data_util, callback_symbols = parse_events(path)

    # plot difference between starts of callbacks

    callback_symbol = list(callback_symbols.items())[0]

    plot_data(data_util, callback_symbol, output_path)

def parse_events(path):
    # Load the trace
    events = load_file(path)

    # Create a handler
    handler = Ros2Handler().process(events)

    data_util = Ros2DataModelUtil(handler.data)

    callback_symbols = data_util.get_callback_symbols()
    return data_util,callback_symbols

def plot_data(data_util, callback_symbol, output_path):
    psize = 450
    colours = ['#29788E', '#DD4968', '#410967']

    earliest_date = None
    obj, symbol = callback_symbol
    duration_df = data_util.get_callback_durations(obj)
    thedate = duration_df.loc[:, 'timestamp'].iloc[0]
    if earliest_date is None or thedate <= earliest_date:
        earliest_date = thedate

    starttime = earliest_date.strftime('%Y-%m-%d %H:%M')

    duration = figure(
        title='Callback start delta',
        x_axis_label=f'start ({starttime})',
        y_axis_label='time since start (ms)',
        width=psize, height=psize,
    )

    colour_i = 0
    # Filter out internal subscriptions
    owner_info = data_util.get_callback_owner_info(obj)
    
    # remnant of loop
    # if not owner_info or '/parameter_events' in owner_info:
    #     continue

    duration_df = data_util.get_callback_durations(obj)

    # sort by timestamp
    duration_df = duration_df.sort_values(by='timestamp')

    # calculate time since previous start
    duration_df['delta'] = duration_df['timestamp'].diff()
    duration_df['delta'] = duration_df['delta'].fillna(timedelta64(0))
    duration_df['diff'] = duration_df['delta'] - duration_df['duration'].shift(1)
    duration_df['diff'] = duration_df['diff'].dt.total_seconds()
    duration_df['diff_in_ms'] = duration_df['diff'] * 1000 # convert to ms
    duration_df

    source = ColumnDataSource(duration_df)
    duration.title.align = 'center'
    duration.line(
        x='timestamp',
        y='diff_in_ms',
        legend_label=str(symbol),
        line_width=2,
        source=source,
        line_color=colours[colour_i],
    )
    colour_i += 1
    duration.legend.label_text_font_size = '11px'
    duration.xaxis[0].formatter = DatetimeTickFormatter(seconds='%Ss')

    # draw a line at the mean and maximum
    mean = duration_df['diff_in_ms'].mean()
    duration.line(
        x=[duration_df['timestamp'].iloc[0], duration_df['timestamp'].iloc[-1]],
        y=[mean, mean],
        line_width=2,
        line_color='black',
        line_dash='dashed',
    )
    duration.line(
        x=[duration_df['timestamp'].iloc[0], duration_df['timestamp'].iloc[-1]],
        y=[duration_df['diff_in_ms'].max(), duration_df['diff_in_ms'].max()],
        line_width=2,
        line_color='red',
        line_dash='dashed',
    )

    # export to html
    output_file(filename=output_path, title='Callback start delta')

    save(duration)


def main():
    # Create an argument parser
    parser = argparse.ArgumentParser(description='Process the path.')

    # Add the path argument
    parser.add_argument('--path', type=str, help='Path to the trace file.')

    parser.add_argument('--output_path', type=str, help='Path where the output will be saved.')

    # Parse the command line arguments
    args = parser.parse_args()

    # Get the path from the parsed arguments
    path = args.path
    output_path = args.output_path

    # Setup tracetools
    setup_tracetools()

    # Parse the events and evaluate
    parse_events_and_evaluate(path, output_path)


if __name__ == "__main__":
    main()