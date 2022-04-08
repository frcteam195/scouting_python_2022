#! /bin/bash

# Script relies on ~/.my.cnf file existing with username and password

basename=$1

if [ -z "$1" ]; then
  echo "You must enter a basename"
  echo "Usage: dbdump.sh nightly"
  exit 1
fi

now=$(date +%Y-%m-%d_%H-%M)

echo "$now"
echo "mysqldump backing up localhost  - saving to "$basename"_"$now".sql"

/usr/bin/mysqldump -u admin -pteam195 team195_scouting > /home/pi/DB-backups/"$basename"_"$now".sql
cd /home/pi/DB-backups
/bin/tar -czf "$basename"_"$now".tgz "$basename"_"$now".sql
/bin/rm /home/pi/DB-backups/"$basename"_"$now".sql

echo 'mysqldump compelte'
echo ''
