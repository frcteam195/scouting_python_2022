/usr/local/mysql/bin/mysqldump --column-statistics=0 --host=frcteam195testinstance.cmdlvflptajw.us-east-1.rds.amazonaws.com --port=3306 \
--user=admin --password=Einstein195 team195_scouting MatchScouting > junk.txt

/usr/local/mysql/bin/mysqlimport --host=frcteam195.cmdlvflptajw.us-east-1.rds.amazonaws.com --port=3306 \
--user=admin --password=Einstein195 team195_scouting MatchScouting < junk.txt

