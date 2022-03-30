#!/usr/bin/env bash

echo ''
echo 'Creating clean log files; analysis.log and dbdump.log'
rm -f /home/pi/analysis.log 
touch /home/pi/analysis.log
chmod a+rw /home/pi/analysis.log
rm -f /home/pi/dbdump.log 
touch /home/pi/dbdump.log
chmod a+rw /home/pi/dbdump.log

echo ''
echo 'Use "crontab -e" to open the crontab file in an editor and edit with vi'
echo ''
echo "*/2 * * * * cd /home/pi && /home/pi/scouting_python_2022/run-analysis.sh >> /home/pi/analysis.log 2>&1"
echo "or on the pi"
echo "*/2 * * * * cd /home/pi && /home/pi/scouting_python_2022/run-analysis-pi.sh >> /home/pi/analysis.log 2>&1"
echo "*/15 * * * * cd /home/pi && /home/pi/scouting_python_2022/dbdump.sh event >> /home/pi/dbdump.log 2>&1"
echo ''

# line to run db dump daily at midnight
# 0 0 * * * cd /home/pi && /home/pi/scouting_python_2022/dbdump.sh daily >> /home/pi/dbdump-daily.log 2>&1
