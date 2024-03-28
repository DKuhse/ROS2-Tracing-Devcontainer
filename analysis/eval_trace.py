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

import os



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
    
    callback_dfs = parse_events(path)

    # create output path if it does not exist
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # dump to pickle
    for callback_id, df in callback_dfs.items():
        df.to_pickle(f"{output_path}/{callback_id}.pkl")

    # write .describe() to file
    with open(f"{output_path}/describe.txt", "w") as f:
        for callback_id, df in callback_dfs.items():
            f.write(f"{callback_id}\n")
            f.write(f"{df.describe()}\n\n")


def parse_events(path):
    # Load the trace
    events = load_file(path)

    callback_dfs = {}

    for event in events:
        if "_name" in event:
            if event["_name"] == "ros2:callback_start":
                timestamp = event["_timestamp"]

                callback_id = event["callback"]

                if callback_id not in callback_dfs:
                    callback_dfs[callback_id] = []

                callback_dfs[callback_id].append({
                    "timestamp": timestamp
                })

    for callback_id, df in callback_dfs.items():
        df = pd.DataFrame(df)

        df["timestamp"] = pd.to_datetime(df["timestamp"])

        callback_dfs[callback_id] = df

    for callback_id, df in callback_dfs.items():
        df["delta"] = df["timestamp"].diff()
        df["delta"] = df["delta"].fillna(pd.Timedelta(seconds=0))
        # to ms
        df["delta"] = df["delta"].dt.total_seconds() * 1000

        callback_dfs[callback_id] = df

    return callback_dfs


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