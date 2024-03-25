mkdir -p traces

# get the current time
now=$(date +"%y_%m_%d__%H:%M:%S")

# Parse command-line options
while getopts ":t:h" opt; do
  case ${opt} in
    t )
      time=$OPTARG
      ;;
    h )
      echo "Usage: run_tracing.sh [-t <time>]"
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
shift $((OPTIND -1))

# Parse positional arguments
if [ $# -gt 0 ]; then
    session_id=$1
fi


if [ -z "$session_id" ]
then
    echo "No session id provided, exiting"
    exit 1
else
    session_name='session_'$session_id
fi





# get the current path and append traces
path=$(pwd)'/traces/'

if [ -z "$time" ]
then
    # just start the tracing
    ros2 trace -p $path -s $session_name
else    
    # execute above expect script
    expect -c "
      spawn ros2 trace -p $path -s $session_name -u ros2:rcl_init ros2:rcl_node_init ros2:rmw_publisher_init ros2:rcl_publisher_init ros2:rmw_subscription_init ros2:rcl_subscription_init ros2:rclcpp_subscription_init ros2:rcl_service_init ros2:rcl_lifecycle_state_machine_init ros2:rclcpp_timer_link_node ros2:rcl_client_init ros2:rcl_timer_init ros2:rclcpp_callback_register ros2:rclcpp_timer_callback_added ros2:rclcpp_service_callback_added ros2:callback_start ros2:callback_end
      expect \"press enter to start...\"
      send \"\r\"
      puts \"\nStarting tracing...\"
      sleep $time
      expect \"press enter to stop...\"
      send \"\r\"
      interact
    "
    echo "Tracing stopped"
fi
