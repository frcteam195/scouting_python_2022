import mysql.connector as mariaDB
import numpy as np
import datetime
import time
import argparse
import sys

tableName = "MatchScouting"


now = datetime.datetime.now()
print(now.strftime("%Y-%m-%d %H:%M:%S"))
start_time = time.time()

# Connection to AWS Testing database - use when you would destroy tables with proper data
connSrc = mariaDB.connect(user='admin',
							passwd='Einstein195',
							host='frcteam195testinstance.cmdlvflptajw.us-east-1.rds.amazonaws.com',
							database='team195_scouting')
cursorSrc = connSrc.cursor()

connDes = mariaDB.connect(user='admin',
							passwd='Einstein195',
							host='frcteam195.cmdlvflptajw.us-east-1.rds.amazonaws.com',
							database='team195_scouting')

cursorDes = connDes.cursor()

# Pi DB with remote access (e.g. from laptop)
# self.conn = mariaDB.connect(user='admin',
#                             passwd='team195',
#                             host='10.0.0.195',
#                             database='team195_scouting')
# self.cursor = self.conn.cursor()

# Pi DB with local access (e.g. from the Pi itself)
# self.conn = mariaDB.connect(user='admin',
#                             passwd='team195',
#                             host='localhost',
#                             database='team195_scouting')
# self.cursor = self.conn.cursor()

# Connection to AWS database with proper data
# self.conn = mariaDB.connect(user='admin',
#                                     passwd='Einstein195',
#                                     host='frcteam195.cmdlvflptajw.us-east-1.rds.amazonaws.com',
#                                     database='team195_scouting')
#         self.cursor = self.conn.cursor()

querySrc = ("SELECT * FROM " + tableName + ";")
print (querySrc)
cursorSrc.execute(querySrc)
rsTableContents = cursorSrc.fetchall()
# print (rsTableContents)


def getTeamData(team):
        self._run_query("SELECT MatchScouting.*, Matches.MatchNo, Teams.RobotWeight "
            "FROM (Events INNER JOIN Matches ON Events.EventID = Matches.EventID) "
            "INNER JOIN MatchScouting ON (Matches.EventID = MatchScouting.EventID) "
            "AND (Matches.MatchID = MatchScouting.MatchID) "
            "INNER JOIN Teams ON (MatchScouting.Team = Teams.Team) "
            "WHERE (((MatchScouting.Team) = " + team[0] + " "
            "AND ((Events.CurrentEvent) = 1))"
            "AND ((ScoutingStatus = 1) Or (ScoutingStatus = 2) Or (ScoutingStatus = 3)) "
            "AND (MatchScouting.TeamMatchNo <= 12)) "
            "ORDER BY MatchScouting.TeamMatchNo;")

        # Set columns to be a list of column headings in the Query results
        # Very cool - cursor.description is used to auto-determine the column headings in the MatchScouting table
        #   so these values do not need to be hard-coded
        self._setColumns([column[0] for column in list(self.cursor.description)])

        rsRobotMatches = self.cursor.fetchall()




wipeTableQuery = ("DELETE FROM " + tableName + ";")
cursorDes.execute(wipeTableQuery)
connDes.commit()

num_rows = len(rsTableContents)
print (num_rows)

setColumns([column[0] for column in list(cursorSrc.description)])

# insertQuery = """INSERT INTO MatchScouting VALUES (%)

# for row in rsTableContents:
#     #print (row)
#     values = str(tuple([record[1] for record in rsTableContents]))
#     print (values)
#     insertTableQuery = ("INSERT INTO " + tableName + "VALUES(" + values + ");")
#     
#     
# cursor = db.cursor()
# vals = [(1,2,3), (4,5,6), (7,8,9), (2,5,6)]
# q = """INSERT INTO first (comments, feed, keyword) VALUES (%s, %s, %s)"""  
# cursor.executemany(q, vals)
#     
# # print (insertTableQuery)
# 
# print("Time: %0.2f seconds" % (time.time() - start_time))
# print()