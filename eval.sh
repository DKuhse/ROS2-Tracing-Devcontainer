# trace the program multiple times

for i in {1..30}
do
    echo "Test $i"
    ./test_and_trace.sh -t 30 -p multi_test -e tester main_$i
    echo "Test $i done"
done