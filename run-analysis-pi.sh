#! /bin/bash

echo '**********************************************************'

echo 'Running BA OPRs'
/usr/bin/python3 /home/pi/scouting_python_2022/BA/Oprs.py -db localhost
echo ''

echo 'Running BA Ranks'
/usr/bin/python3 /home/pi/scouting_python_2022/BA/Ranks.py -db localhost
echo ''

echo 'Running BA MatchData'
/usr/bin/python3 /home/pi/scouting_python_2022/BA/MatchData.py -db localhost
echo ''

echo 'Running copyBAMatchData'
/usr/bin/python3 /home/pi/scouting_python_2022/copyBAMatchData.py -db localhost
echo ''

echo 'Running SheetsLvl2Scouting'
/usr/bin/python3 /home/pi/scouting_python_2022/SheetsLvl2Scouting.py -db localhost
echo ''

echo 'Running analysisIR'
/usr/bin/python3 /home/pi/scouting_python_2022/analysisIR.py -db localhost

echo 'Running graphIR'
/usr/bin/python3 /home/pi/scouting_python_2022/graphIR.py -db localhost

echo 'Running mysqldump'
/usr/bin/mysqldump -u admin -pteam195 team195_scouting > /home/pi/DB-backups/dbdump.sql
/bin/sleep 1
#/bin/tar -czf dbdump.sql.tgz
#/bin/sleep 1
echo ''

echo 'Running mysql to copy database to AWS-dev'
db=frcteam195testinstance.cmdlvflptajw.us-east-1.rds.amazonaws.com
/usr/bin/mysql -h $db -u admin -pEinstein195 team195_scouting < /home/pi/DB-backups/dbdump.sql
echo ''
