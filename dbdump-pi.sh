#! /bin/bash

# Script relies on ~/.my.cnf file existing with username and password

basename=$1
database=$2

if [ -z "$1" ]; then
  echo "You must enter a basename and database"
  echo "Usage: dbdump.sh nightly aws-dev"
  exit 1
fi

if [ -z "$2" ]; then
  echo "You must enter a basename and database"
  echo "Usage: dbdump.sh backup localhost"
  exit 1
fi

now=$(date +%Y-%m-%d_%H-%M)

if [ $database = 'aws-dev' ]; then
  # db=frcteam195.cmdlvflptajw.us-east-1.rds.amazonaws.com
  db=frcteam195testinstance.cmdlvflptajw.us-east-1.rds.amazonaws.com
elif [ $database = 'localhost' ]; then
  db=localhost
else
  echo 'You must select aws-dev or localhost'
  exit 1
fi

echo "$now"
echo "mysqldump backing up "$database"  - saving to "$basename"_"$now".sql"

/usr/bin/mysqldump -h "$db" team195_scouting > /home/pi/DB-backups/"$basename"_"$now".sql

echo 'mysqldump compelte'
echo ''
