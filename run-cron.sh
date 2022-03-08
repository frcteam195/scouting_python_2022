#! /usr/bin/bash

echo 'Running analysisIR'
/usr/bin/python3 /home/nmrbox/mmaciejewski/scouting/scouting_python_2022/analysisIR.py -db aws-dev

echo 'Running graphIR'
/usr/bin/python3 /home/nmrbox/mmaciejewski/scouting/scouting_python_2022/graphIR.py -db aws-dev
