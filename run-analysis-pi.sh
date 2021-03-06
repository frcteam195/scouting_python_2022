#! /bin/bash

# Use this script as a cron job when utilizing Raspberry Pi with good Internet
#   bandwidth as the primary database for data collection. Script runs all the 
#   BA and Google scripts as well as the standard analysis and graph scripts. 
#   In addition, it pushes appropriate tables to AWS-dev for the public website

# As the regular pi user, use crontab -e to edit the crontab file for pi
# */4 * * * * cd /home/pi && /home/pi/scouting_python_2022/run-analysis-pi.sh >> /home/pi/analysis.log 2>&1
# NOTE: Run the ./cron-service.sh script first to create the /home/pi/analysis.log file
#       and view directions for how to start the cron job

echo '**********************************************************'
total_start_time=$(date +%s)

echo 'Running BA OPRs'
/usr/bin/python3 /home/pi/scouting_python_2022/BA/Oprs.py -db localhost

echo 'Running BA Ranks'
/usr/bin/python3 /home/pi/scouting_python_2022/BA/Ranks.py -db localhost

echo 'Running BA MatchData'
/usr/bin/python3 /home/pi/scouting_python_2022/BA/MatchData.py -db localhost

echo 'Running copyBAMatchData'
/usr/bin/python3 /home/pi/scouting_python_2022/copyBAMatchData.py -db localhost

echo 'Running insertFouls to add fouls and Ranking point data'
/usr/bin/python3 /home/pi/scouting_python_2022/insertFouls.py -db localhost

echo 'Running SheetsLvl2Scouting'
/usr/bin/python3 /home/pi/scouting_python_2022/SheetsLvl2Scouting.py -db localhost

echo 'Running insertRobotImage.py'
/usr/bin/python3 /home/pi/scouting_python_2022/insertRobotImage.py -db localhost

echo 'Running analysisIR'
/usr/bin/python3 /home/pi/scouting_python_2022/analysisIR.py -db localhost

echo 'Running graphIR'
/usr/bin/python3 /home/pi/scouting_python_2022/graphIR.py -db localhost

echo 'Creating DB dump for entire DB as a backup with mysqldump'
/home/pi/scouting_python_2022/dbdump-pi.sh event

total_end_time=$(date +%s)
total_elapsed=$(( total_end_time - total_start_time ))
echo "Total Run Time: $total_elapsed seconds"
echo ''

