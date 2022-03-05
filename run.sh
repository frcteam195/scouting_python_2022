#! /bin/bash

i=1

while [ $i -le  10 ]
do
    echo "Running $i of 10"
    python3 analysisIR.py -db aws-dev
    python3 graphIR.py -db aws-dev
    sleep 60
    i=$(( $i + 1 ))
done

