import mysql.connector as mariaDB
import numpy as np
import datetime
import time
import argparse
import sys

table_name = "MatchScouting"

now = datetime.datetime.now()
print(now.strftime("%Y-%m-%d %H:%M:%S"))
start_time = time.time()

# Connection to AWS Testing database - use when you would destroy tables with proper data
connSrc = mariaDB.connect(user='admin',
						   passwd='Einstein195',
							host='frcteam195testinstance.cmdlvflptajw.us-east-1.rds.amazonaws.com',
						   database='team195_scouting')
cursorSrc = connSrc.cursor()

# Pi DB with remote access (e.g. from laptop)
# conn = mariaDB.connect(user='admin',
							# passwd='team195',
							# host='10.0.0.195',
							# database='team195_scouting')
# cursor = conn.cursor()

# Pi DB with local access (e.g. from the Pi itself)
# conn = mariaDB.connect(user='admin',
							# passwd='team195',
							# host='localhost',
							# database='team195_scouting')
# cursor = conn.cursor()

# Connection to AWS database with proper data
connDes = mariaDB.connect(user='admin',
							passwd='Einstein195',
							host='frcteam195.cmdlvflptajw.us-east-1.rds.amazonaws.com',
							database='team195_scouting')
cursorDes = connDes.cursor()

columns = []
#wipeTable()
#rsRobots = getTeams()
#analyzeTeams()

print("Time: %0.2f seconds" % (time.time() - start_time))
print()

# # Function to run a query - the query string must be passed to the function
# def run_query(query):
    # cursor.execute(query)

# # Function to determine the DB table column headers
# def setColumns(columns):
    # columns = columns

# # Function to wipe the CEA table. We may want to make this only remove CurrentEvent records.
# def wipeTable():
    # run_query("DELETE FROM " + table_name + ";")
    # conn.commit()

# # Function to get the team list and set it to rsRobots. Uses the _run_query function defined above.
# #   The assert statement will return rsRobots if the record length > 0 and will exit with the
# #       message "No robots founds" if the record length is 0.
# def getTeams:
    # run_query("SELECT MatchScouting.Team FROM (MatchScouting "
                   # "INNER JOIN Matches ON MatchScouting.MatchID = Matches.MatchID) "
                   # "INNER JOIN Events ON Matches.EventID = Events.EventID "
                   # "WHERE (((Events.CurrentEvent) = 1)) "
                   # "GROUP BY CAST(MatchScouting.Team AS INT), MatchScouting.Team "
                   # "HAVING (((MatchScouting.Team) Is Not Null)); ")
    # rsRobots = cursor.fetchall()

    # assert len(rsRobots) > 0, "No robots found"
    # return rsRobots

# # Function to retrieve data records for a given team for all their matches and set it to rsRobotMatches
# def getTeamData(team):
    # run_query("SELECT MatchScouting.*, Matches.MatchNo, Teams.RobotWeight "
        # "FROM (Events INNER JOIN Matches ON Events.EventID = Matches.EventID) "
        # "INNER JOIN MatchScouting ON (Matches.EventID = MatchScouting.EventID) "
        # "AND (Matches.MatchID = MatchScouting.MatchID) "
        # "INNER JOIN Teams ON (MatchScouting.Team = Teams.Team) "
        # "WHERE (((MatchScouting.Team) = " + team[0] + " "
        # "AND ((Events.CurrentEvent) = 1))"
        # "AND ((ScoutingStatus = 1) Or (ScoutingStatus = 2) Or (ScoutingStatus = 3)) "
        # "AND (MatchScouting.TeamMatchNo <= 12)) "
        # "ORDER BY MatchScouting.TeamMatchNo;")

    # # Set columns to be a list of column headings in the Query results
    # # Very cool - cursor.description is used to auto-determine the column headings in the MatchScouting table
    # #   so these values do not need to be hard-coded
    # setColumns([column[0] for column in list(cursor.description)])

    # rsRobotMatches = cursor.fetchall()

    # # If rsRobotMatches is not zero length return rsRobotMatches otherwise return None. This allows the
    # #   function to skip a robot analysis if that robot does not have any match records yet.
    # if rsRobotMatches:
        # return rsRobotMatches
    # else:
        # return None

# #
# def analyzeTeams():
    # # Loop over the # of teams and run each of the analysis functions calling _insertAnalysis after each one is run
    # for team in self.rsRobots:
        # # print(team)
        # rsRobotMatches = getTeamData(team)
        # # print(rsRobotMatches

        # if rsRobotMatches:
            # rsTable = startingPosition(rsRobotMatches=rsRobotMatches)
            # self._insertAnalysis(rsTable)
            
# # Function to insert an rsTable record into the DB.
# def insertAnalysis(rsTable):
    # rsTable_records = rsTable.items()
    # # Get the columnHeadings and values, do some formatting, and then use the _run_query function to run the
    # #   query and the conn.commit to insert into the DB.
    # columnHeadings = str(tuple([record[0] for record in rsTable_records])).replace("'", "")
    # values = str(tuple([record[1] for record in rsTable_records]))

    # # Insert the records into the DB
    # run_query("INSERT INTO " + table_name + " "
                    # + columnHeadings + " VALUES "
                    # + values + ";")
    # # print(columnHeadings + values)
    # conn.commit()

