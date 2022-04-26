#! /usr/bin/bash

# Use this script as a cron job when utilizing AWS-dev as the primary database
#   for data collection. Script runs all the BA and Google scripts as well
#   as the standard analysis and graph scripts. In addition, it creates backups
#   of the database with mysqldump

# As the regular pi user, use crontab -e to edit the crontab file for pi
# */2 * * * * cd /home/pi && /home/pi/scouting_python_2022/run-analysis.sh >> /home/pi/analysis.log 2>&1
# NOTE: Run the ./cron-service.sh script first to create the /home/pi/analysis.log file
#       and view directions for how to start the cron job

echo '**********************************************************'

echo 'Running BA OPRs'
/usr/bin/python3 /home/pi/scouting_python_2022/BA/Oprs.py -db aws-dev

echo 'Running BA Ranks'
/usr/bin/python3 /home/pi/scouting_python_2022/BA/Ranks.py -db aws-dev

echo 'Running BA MatchData'
/usr/bin/python3 /home/pi/scouting_python_2022/BA/MatchData.py -db aws-dev

echo 'Running copyBAMatchData'
/usr/bin/python3 /home/pi/scouting_python_2022/copyBAMatchData.py -db aws-dev

echo 'Running insertFouls to add fouls and Ranking point data'
/usr/bin/python3 /home/pi/scouting_python_2022/insertFouls.py -db aws-dev

echo 'Running SheetsLvl2Scouting'
/usr/bin/python3 /home/pi/scouting_python_2022/SheetsLvl2Scouting.py -db aws-dev

echo 'Running analysisIR'
/usr/bin/python3 /home/pi/scouting_python_2022/analysisIR.py -db aws-dev

echo 'Running graphIR'
/usr/bin/python3 /home/pi/scouting_python_2022/graphIR.py -db aws-dev

echo 'Creating DB dump for entire DB as a backup with mysqldump'
/home/pi/scouting_python_2022/dbdump.sh event

# echo 'Running mysqldump to dump local DB to dbdump.sql'
# start_time=$(date +%s)
# /usr/bin/mysqldump -u admin -pxxx team195_scouting > /home/pi/DB-backups/dbdump.sql
# /bin/sleep 1
# end_time=$(date +%s)
# elapsed=$(( end_time - start_time ))
# echo "Time: $elapsed seconds"
# #/bin/tar -czf dbdump.sql.tgz
# #/bin/sleep 1
# echo ''
# 
# echo 'Running mysql to copy database to AWS-dev'
# start_time=$(date +%s)
# db=frcteam195testinstance.cmdlvflptajw.us-east-1.rds.amazonaws.com
# /usr/bin/mysql -h $db -u admin -pxxx team195_scouting < /home/pi/DB-backups/dbdump.sql
# end_time=$(date +%s)
# elapsed=$(( end_time - start_time ))
# echo "Time: $elapsed seconds"
# echo ''
