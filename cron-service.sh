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
echo 'Use "crontab -l" to view the current crontab file'
echo 'Use "crontab -e" to open the crontab file in an editor and edit with vi'
echo ''
echo 'When using AWS-dev as the primary DB for the scouting system,'
echo 'on markdev20.nmrbox.org, use this line:'
echo "*/3 * * * * cd /home/pi && /home/pi/scouting_python_2022/run-analysis.sh >> /home/pi/analysis.log 2>&1"
echo ''
echo 'When using the Raspberry Pi as the primary DB for the scouting system with good bandwidth,'
echo 'on the Raspbery Pi, use this line:'
echo "*/3 * * * * cd /home/pi && /home/pi/scouting_python_2022/run-analysis-pi.sh >> /home/pi/analysis.log 2>&1"
echo ''
echo 'To create nightly backups of AWS-dev run this line on markdev20.nmrbox.org:'
echo '0 0 * * * cd /home/pi && /home/pi/scouting_python_2022/dbdump.sh daily >> /home/pi/dbdump-daily.log 2>&1'
echo ''