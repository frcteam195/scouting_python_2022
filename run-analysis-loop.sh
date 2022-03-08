#! /bin/bash

i=1

while [ $i -le  10 ]
do
    echo "Running $i of 10"
    ./run-analysis.sh
    sleep 60
    i=$(( $i + 1 ))
done

