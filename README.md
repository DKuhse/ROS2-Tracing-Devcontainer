# ROS2-Tracing-Devcontainer

## Setup

Install [Docker Engine](https://docs.docker.com/engine/install/)

Install [Visual Studio Code](https://code.visualstudio.com/)

## Start the Container with Visual Studio Code

In Visual Studio Code, install the **Docker** and **Dev Containers** extensions.

Build and open the container.

## Start the Container with Docker

Run the following command in a terminal that is in the current folder's directory:

> docker build -t ros2-tracing .devcontainer/

Start the container using the following command:

> docker run --network host -it -v .:/home/vscode/workspace ros2-tracing

## Tracing

The trace tools are already set up. Execute the run_tracing.sh script to start tracing. You can specify a command line argument to set the folder name of the trace in the traces folder.

>./run_tracing.sh -t <time_in_seconds> <session_name>

To automatically start the executable and trace at the same time

>./test_and_trace.sh -t <time_in_seconds> -p <package_name> -e <executable_name> <session_name>

Evaluate it multiple times


>./eval.sh -n <iteration_count> -t <time_in_seconds> [-p <package>] [-e <executable>] [-s <session_name>]


## Plotting
Plots the time between callbacks into an html file, reading the recorded trace folder.

>python3 ./analysis/eval_trace --path <path_to_trace_folder> --output_path <path_to_output_html_file>
