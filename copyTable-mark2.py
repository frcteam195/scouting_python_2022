import mysql.connector as mariaDB
import numpy as np
import datetime
import time
import argparse
import sys


CEA_table = "MatchScouting"

# Define a Class called analysis
class analysis():
    # Inside the class there are several functions defined _run_query, _setColumns, _wipeCEA, _getTeams,
    #   _getTeamData, _analyzeTeams, and _insertAnalysis. Those functions will not get called automatically
    #   so in order to get them to run we create a __init__ function which is a special function in Python
    #   that gets run every time the Class is initialized. Here we build the DB connection cursor from within
    #   the __init__ function and then call the cursor, columns, wipeCEA, rsRobots, and analyzeTeams functions
    #   from within the __init__ function, which means they will be run automatically when the Class is initialized
    def __init__(self):
        now = datetime.datetime.now()
        print(now.strftime("%Y-%m-%d %H:%M:%S"))
        start_time = time.time()
        
        # Connection to AWS Testing database
        connSrc = mariaDB.connect(user='admin',
						    passwd='Einstein195',
						    host='frcteam195testinstance.cmdlvflptajw.us-east-1.rds.amazonaws.com',
						    database='team195_scouting')
        cursorSrc = connSrc.cursor()

        # Connection to AWS database with proper data
        connDes = mariaDB.connect(user='admin',
							passwd='Einstein195',
							host='frcteam195.cmdlvflptajw.us-east-1.rds.amazonaws.com',
							database='team195_scouting')
        cursorDes = connDes.cursor()

        self.columns = []
        self._wipeCEA()
        self._getTable()

        print("Time: %0.2f seconds" % (time.time() - start_time))
        print()

    # Function to run a query - the query string must be passed to the function
    def _run_querySrc(self, query):
        self.cursorSrc.execute(query)

    def _run_queryDes(self, query):
        self.cursorDes.execute(query)

    # Function to determine the DB table column headers
    def _setColumns(self, columns):
        self.columns = columns

    # Function to wipe the CEA table. We may want to make this only remove CurrentEvent records.
    def _wipeCEA(self):
        self._run_query("DELETE FROM " + CEA_table + ";")
        self.connDes.commit()

    """ def _getTable(self):
        self._run_querySrc("SELECT * FROM MatchScouting")
        rsTable = self.cursorSrc.fetchall()

        assert len(rsTable) > 0, "No records"
        return rsTable """

    # Function to retrieve data records for a given team for all their matches and set it to rsRobotMatches
    def _getTable(self):
        self._run_querySrc("SELECT * FROM MatchScouting;")
        self._setColumns([column[0] for column in list(self.cursor.description)])

        rsRobotMatches = self.cursor.fetchall()

        if rsRobotMatches:
            return rsRobotMatches
        else:
            return None

    #
    """ def _analyzeTeams(self):
        # Loop over the # of teams and run each of the analysis functions calling _insertAnalysis after each one is run
        for team in self.rsRobots:
            # print(team)
            rsRobotMatches = self._getTeamData(team)
            # print(rsRobotMatches)

            if rsRobotMatches:
                rsCEA = startingPosition(analysis=self, rsRobotMatches=rsRobotMatches)
                self._insertAnalysis(rsCEA)
 """

    # Function to insert an rsCEA record into the DB.
    def _insertAnalysis(self, rsRobotMatches):
        rsRobotMatches_records = rsRobotMatches.items()
        columnHeadings = str(tuple([record[0] for record in rsRobotMatches_records])).replace("'", "")
        values = str(tuple([record[1] for record in rsRobotMatches_records]))

        # Insert the records into the DB
        self._run_query("INSERT INTO " + CEA_table + " "
                        + columnHeadings + " VALUES "
                        + values + ";")
        # print(columnHeadings + values)
        self.connDes.commit()


# This initizlzes the analysis Class and thus runs the program.
if __name__ == '__main__':
    myAnalysis = analysis()
    