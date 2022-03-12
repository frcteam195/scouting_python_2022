#! /usr/bin/bash

echo 'Running analysisIR'
/usr/bin/python3 /home/pi/scouting_python_2022/analysisIR.py -db localhost

echo 'Running graphIR'
/usr/bin/python3 /home/pi/scouting_python_2022/graphIR.py -db localhost

echo 'Running copyTable'
/usr/bin/python3 /home/pi/scouting_python_2022/copyTable.py -dbs localhost -dbd aws-dev -table MotorTypes
