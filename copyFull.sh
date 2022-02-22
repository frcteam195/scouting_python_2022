#! /bin/bash

rm -f copyFull.log

python3 copyTable.py -dbs aws-dev -dbd aws-prod  -table AllianceStations >> copyFull.log
echo 'AllianceStations'
python3 copyTable.py -dbs aws-dev -dbd aws-prod  -table AnalysisTypes >> copyFull.log
echo 'AnalysisTypes'
python3 copyTable.py -dbs aws-dev -dbd aws-prod  -table BlueAllianceEvents >> copyFull.log
echo 'BlueAllianceEvents'
python3 copyTable.py -dbs aws-dev -dbd aws-prod  -table BlueAllianceOPR >> copyFull.log
echo 'BlueAllianceOPR'
python3 copyTable.py -dbs aws-dev -dbd aws-prod  -table BlueAllianceRankings >> copyFull.log
echo 'BlueAllianceRankings'
python3 copyTable.py -dbs aws-dev -dbd aws-prod  -table BlueAllianceSchedule >> copyFull.log
echo 'BlueAllianceSchedule'
python3 copyTable.py -dbs aws-dev -dbd aws-prod  -table BlueAllianceTeams >> copyFull.log
echo 'BlueAllianceTeams'
python3 copyTable.py -dbs aws-dev -dbd aws-prod  -table ClimbStatus >> copyFull.log
echo 'ClimbStatus'
python3 copyTable.py -dbs aws-dev -dbd aws-prod  -table ColorTypes >> copyFull.log
echo 'ColorTypes'
python3 copyTable.py -dbs aws-dev -dbd aws-prod  -table Computers >> copyFull.log
echo 'Computers'
python3 copyTable.py -dbs aws-dev -dbd aws-prod  -table ComputerTypes >> copyFull.log
echo 'ComputerTypes'
python3 copyTable.py -dbs aws-dev -dbd aws-prod  -table CurrentEventTeams >> copyFull.log
echo 'CurrentEventTeams'
python3 copyTable.py -dbs aws-dev -dbd aws-prod  -table DriveTypes >> copyFull.log
echo 'DriveTypes'
python3 copyTable.py -dbs aws-dev -dbd aws-prod  -table Events >> copyFull.log
echo 'Events'
python3 copyTable.py -dbs aws-dev -dbd aws-prod  -table LanguageTypes >> copyFull.log
echo 'LanguageTypes'
python3 copyTable.py -dbs aws-dev -dbd aws-prod  -table Matches >> copyFull.log
echo 'Matches'
python3 copyTable.py -dbs aws-dev -dbd aws-prod  -table MatchScouting >> copyFull.log
echo 'MatchScouting'
python3 copyTable.py -dbs aws-dev -dbd aws-prod  -table MatchScoutingL2 >> copyFull.log
echo 'MatchScoutingL2'
python3 copyTable.py -dbs aws-dev -dbd aws-prod  -table MotorTypes >> copyFull.log
echo 'MotorTypes'
python3 copyTable.py -dbs aws-dev -dbd aws-prod  -table Teams >> copyFull.log
echo 'Teams'
python3 copyTable.py -dbs aws-dev -dbd aws-prod  -table Users >> copyFull.log
echo 'Users'
python3 copyTable.py -dbs aws-dev -dbd aws-prod  -table WheelTypes >> copyFull.log
echo 'WheelTypes'
python3 copyTable.py -dbs aws-dev -dbd aws-prod  -table WordCloud >> copyFull.log
echo 'WordCloud'
python3 copyTable.py -dbs aws-dev -dbd aws-prod  -table WordID >> copyFull.log
echo 'WordID'

echo 'Harish approved'
