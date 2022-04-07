#! /usr/bin/bash

# Script relies on ~/.my.cnf file existing with username and password

basename=$1

if [ -z "$1" ]; then
  echo "You must enter a basename"
  echo "Usage: dbdump.sh nightly"
  exit 1
fi

now=$(date +%Y-%m-%d_%H-%M)

echo "$now"
echo "mysqldump starting - saving to "$basename"_"$now".sql"

# db=frcteam195.cmdlvflptajw.us-east-1.rds.amazonaws.com
db=frcteam195testinstance.cmdlvflptajw.us-east-1.rds.amazonaws.com

/usr/bin/mysqldump -h "$db" team195_scouting > /home/pi/DB-backups/"$basename"_"$now".sql
/usr/bin/tar -czf /home/pi/DB-backups/"$basename"_"$now".tgz /home/pi/DB-backups/"$basename"_"$now".sql
/usr/bin/rm /home/pi/DB-backups/"$basename"_"$now".sql

echo 'mysqldump compelte'
echo ''
