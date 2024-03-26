# runs run_tracing.sh -t $time $session_id
# then executes ros2 run $package $executable
# terminate the process after the given time

# parse command-line options (-t, -p, -e)
while getopts ":t:p:e:h" opt; do
    case ${opt} in
        t )
            time=$OPTARG
            ;;
        p )
            package=$OPTARG
            ;;
        e )
            executable=$OPTARG
            ;;
        h )
            echo "Usage: test_and_trace.sh [-t <time>] [-p <package>] [-e <executable>] [-h]"
            echo "Options:"
            echo "  -t <time>        Specify the time to run the tracing"
            echo "  -p <package>     Specify the package to run"
            echo "  -e <executable>  Specify the executable to run"
            echo "  -h               Display this help message"
            exit 0
            ;;
        \? )
            echo "Invalid option: $OPTARG" 1>&2
            ;;
        : )
            echo "Invalid option: $OPTARG requires an argument" 1>&2
            ;;
    esac
done

# shift the options so that the positional arguments can be parsed
shift $((OPTIND -1))

# parse positional arguments
if [ $# -gt 0 ]; then
    session_id=$1
fi

echo "Running the package $package with the executable $executable for $time seconds, session id: $session_id"

# execute run_tracing.sh -t $time $session_id, send enter key to the process, sleep for 5 seconds, send enter key to the process
source ./run_tracing.sh -t $time $session_id &

source ./packages/install/setup.sh

sleep 5

# execute the package and executable, suppress output, terminate the process after the given time
timeout $time ros2 run $package $executable