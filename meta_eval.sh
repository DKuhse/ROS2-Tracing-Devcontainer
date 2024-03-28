cd packages/rclcpp_multi_test

echo "Reverting the fix"

git checkout main

cd ..

colcon build --symlink-install

cd ~/workspace

./eval.sh -n 3 -t 300 -s unfixed_var1

cd packages/rclcpp_multi_test

echo "Applying the fix"

git checkout advanced_fix_mutex_no_waiting

cd ..

colcon build --symlink-install

cd ~/workspace

./eval.sh -n 3 -t 300 -s fixed_var1