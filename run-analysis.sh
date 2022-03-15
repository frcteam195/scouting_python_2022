#! /usr/bin/bash

echo '**********************************************************'

echo 'Running BA OPRs'
/usr/bin/python3 /home/pi/scouting_python_2022/BA/Oprs.py -db aws-dev

echo ''

echo 'Running BA Ranks'
/usr/bin/python3 /home/pi/scouting_python_2022/BA/Ranks.py -db aws-dev


echo 'Running analysisIR'
/usr/bin/python3 /home/pi/scouting_python_2022/analysisIR.py -db aws-dev

echo 'Running graphIR'
/usr/bin/python3 /home/pi/scouting_python_2022/graphIR.py -db aws-dev

