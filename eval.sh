# trace the program multiple times

# parse command line arguments
iteration_count=30
time_in_seconds=30
package="multi_test"
executable="tester"
session_name="main"

while getopts "n:t:p:e:s:" opt; do
    case $opt in
        n)
            iteration_count=$OPTARG
            ;;
        t)
            time_in_seconds=$OPTARG
            ;;
        p)
            package=$OPTARG
            ;;
        e)
            executable=$OPTARG
            ;;
        s)
            session_name=$OPTARG
            ;;
        \?)
            echo "Invalid option: -$OPTARG" >&2
            exit 1
            ;;
    esac
done

# validate arguments
if [[ -z $iteration_count || -z $time_in_seconds ]]; then
    echo "Missing arguments. Usage: $0 -n <iteration_count> -t <time_in_seconds> [-p <package>] [-e <executable>] [-s <session_name>]"
    exit 1
fi

# rest of the code
for ((i = 1; i <= $iteration_count; i++))
do
        echo "Test $i"
        ./test_and_trace.sh -t $time_in_seconds -p $package -e $executable ${session_name}_$i
        echo "Test $i done"
        sleep 15
done

# output the results
for ((i = 1; i <= $iteration_count; i++))
do
        python3 /home/vscode/workspace/analysis/eval_trace.py --path /home/vscode/workspace/traces/session_${session_name}_$i --output_path /home/vscode/workspace/output/${session_name}_$i/
done