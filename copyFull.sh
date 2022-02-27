#! /bin/bash

rm -f copyFull.log

if [[ $# -ne 2 ]]; then
    echo "Illegal number of arguments. Enter a DB source and DB destination" >&2
    exit 2
fi

sourceDB=$1
destinationDB=$2
echo ''
echo "Using $sourceDB as source DB"
echo "Using $destinationDB as destinatiuon DB"
echo ''
echo "Copying tables ..."

# echo "python3 copyTable.py -dbs $sourceDB -dbd $destinationDB  -table AllianceStations >> copyFull.log"

    echo 'AllianceStations'
python3 copyTable.py -dbs $sourceDB -dbd $destinationDB  -table AllianceStations >> copyFull.log
    echo 'AnalysisTypes'
python3 copyTable.py -dbs $sourceDB -dbd $destinationDB  -table AnalysisTypes >> copyFull.log
    echo 'BlueAllianceEvents'
python3 copyTable.py -dbs $sourceDB -dbd $destinationDB  -table BlueAllianceEvents >> copyFull.log
    echo 'BlueAllianceOPR'
python3 copyTable.py -dbs $sourceDB -dbd $destinationDB  -table BlueAllianceOPR >> copyFull.log
    echo 'BlueAllianceRankings'
python3 copyTable.py -dbs $sourceDB -dbd $destinationDB  -table BlueAllianceRankings >> copyFull.log
    echo 'BlueAllianceSchedule'
python3 copyTable.py -dbs $sourceDB -dbd $destinationDB  -table BlueAllianceSchedule >> copyFull.log
    echo 'BlueAllianceTeams'
python3 copyTable.py -dbs $sourceDB -dbd $destinationDB  -table BlueAllianceTeams >> copyFull.log
    echo 'ClimbStatus'
python3 copyTable.py -dbs $sourceDB -dbd $destinationDB  -table ClimbStatus >> copyFull.log
    echo 'ColorTypes'
python3 copyTable.py -dbs $sourceDB -dbd $destinationDB  -table ColorTypes >> copyFull.log
    echo 'Computers'
python3 copyTable.py -dbs $sourceDB -dbd $destinationDB  -table Computers >> copyFull.log
    echo 'ComputerTypes'
python3 copyTable.py -dbs $sourceDB -dbd $destinationDB  -table ComputerTypes >> copyFull.log
    echo 'CurrentEventTeams'
python3 copyTable.py -dbs $sourceDB -dbd $destinationDB  -table CurrentEventTeams >> copyFull.log
    echo 'DriveTypes'
python3 copyTable.py -dbs $sourceDB -dbd $destinationDB  -table DriveTypes >> copyFull.log
    echo 'Events'
python3 copyTable.py -dbs $sourceDB -dbd $destinationDB  -table Events >> copyFull.log
    echo 'LanguageTypes'
python3 copyTable.py -dbs $sourceDB -dbd $destinationDB  -table LanguageTypes >> copyFull.log
    echo 'Matches'
python3 copyTable.py -dbs $sourceDB -dbd $destinationDB  -table Matches >> copyFull.log
    echo 'MatchScouting'
python3 copyTable.py -dbs $sourceDB -dbd $destinationDB  -table MatchScouting >> copyFull.log
    echo 'MatchScoutingL2'
python3 copyTable.py -dbs $sourceDB -dbd $destinationDB  -table MatchScoutingL2 >> copyFull.log
    echo 'MotorTypes'
python3 copyTable.py -dbs $sourceDB -dbd $destinationDB  -table MotorTypes >> copyFull.log
    echo 'Teams'
python3 copyTable.py -dbs $sourceDB -dbd $destinationDB  -table Teams >> copyFull.log
    echo 'Users'
python3 copyTable.py -dbs $sourceDB -dbd $destinationDB  -table Users >> copyFull.log
    echo 'WheelTypes'
python3 copyTable.py -dbs $sourceDB -dbd $destinationDB  -table WheelTypes >> copyFull.log
    echo 'WordCloud'
python3 copyTable.py -dbs $sourceDB -dbd $destinationDB  -table WordCloud >> copyFull.log
    echo 'WordID'
python3 copyTable.py -dbs $sourceDB -dbd $destinationDB  -table WordID >> copyFull.log


echo ''
echo 'Harish approved'
echo ''
