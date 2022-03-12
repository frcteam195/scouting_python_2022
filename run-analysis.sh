#! /bin/bash

date

echo 'Running analysisIR'
/usr/bin/python3 /home/pi/scouting_python_2022/analysisIR.py -db localhost

echo 'Running graphIR'
/usr/bin/python3 /home/pi/scouting_python_2022/graphIR.py -db localhost

echo 'Copying CurrentEventAnalysisGraphs'
/usr/bin/python3 /home/pi/scouting_python_2022/copyTable.py -dbs localhost -dbd aws-dev -table CurrentEventAnalysis

echo 'Copying CurrentEventAnalysisGraphs'
/usr/bin/python3 /home/pi/scouting_python_2022/copyTable.py -dbs localhost -dbd aws-dev -table CurrentEventAnalysisGraphs

#echo 'Copying Matches'
#/usr/bin/python3 /home/pi/scouting_python_2022/copyTable.py -dbs localhost -dbd aws-dev -table Matches

echo 'Copying WordCloud'
/usr/bin/python3 /home/pi/scouting_python_2022/copyTable.py -dbs localhost -dbd aws-dev -table WordCloud

echo 'Copying WordCloudID'
/usr/bin/python3 /home/pi/scouting_python_2022/copyTable.py -dbs localhost -dbd aws-dev -table WordCloudID

echo 'Copying Teams'
/usr/bin/python3 /home/pi/scouting_python_2022/copyTable.py -dbs localhost -dbd aws-dev -table Teams

date
