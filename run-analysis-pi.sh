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

echo 'Running analysisIR'
/usr/bin/python3 /home/pi/scouting_python_2022/analysisIR.py -db localhost

echo 'Running graphIR'
/usr/bin/python3 /home/pi/scouting_python_2022/graphIR.py -db localhost

echo 'Creating DB dump for entire DB as a backup with mysqldump'
/home/pi/scouting_python_2022/dbdump-pi.sh event

echo 'Running mysqldump to push select tables to AWS-dev'
start_time=$(date +%s)
/usr/bin/mysqldump -u admin -pteam195 team195_scouting \
--ignore-table=team195_scouting.Final24 \
--ignore-table=team195_scouting.DnpList \
--ignore-table=team195_scouting.PickList1 \
--ignore-table=team195_scouting.Watch1 \
--ignore-table=team195_scouting.Watch2 \
--ignore-table=team195_scouting.Teams \
--ignore-table=team195_scouting.AnalysisTypes \
--ignore-table=team195_scouting.WheelTypes \
--ignore-table=team195_scouting.DriveTypes \
--ignore-table=team195_scouting.MotorTypes \
--ignore-table=team195_scouting.LanguageTypes \
--ignore-table=team195_scouting.WordID \
--ignore-table=team195_scouting.Users \
--ignore-table=team195_scouting.AdHocMatchReport \
--ignore-table=team195_scouting.AllianceStations \
--ignore-table=team195_scouting.BlueAllianceEvents \
--ignore-table=team195_scouting.ClimbStatus \
--ignore-table=team195_scouting.ColorTypes \
--ignore-table=team195_scouting.MatchScoutingL2 \
--ignore-table=team195_scouting.ScorePredictor \
--ignore-table=team195_scouting.ScorePredictorData > /home/pi/DB-backups/dbdump.sql
/bin/sleep 1
end_time=$(date +%s)
elapsed=$(( end_time - start_time ))
echo "Time: $elapsed seconds"
#/bin/tar -czf dbdump.sql.tgz
#/bin/sleep 1
echo ''

echo 'Running mysql to copy database to AWS-dev'
start_time=$(date +%s)
db=frcteam195testinstance.cmdlvflptajw.us-east-1.rds.amazonaws.com
/usr/bin/mysql -h $db -u admin -pEinstein195 team195_scouting < /home/pi/DB-backups/dbdump.sql
end_time=$(date +%s)
elapsed=$(( end_time - start_time ))
echo "Time: $elapsed seconds"
echo ''

total_end_time=$(date +%s)
total_elapsed=$(( total_end_time - total_start_time ))
echo "Total Run Time: $total_elapsed seconds"
echo ''

