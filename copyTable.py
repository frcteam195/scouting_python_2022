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

        # Connection to AWS Testing database - use when you would destroy tables with proper data
        self.conn = mariaDB.connect(user='admin',
                                    passwd='Einstein195',
                                    host='frcteam195testinstance.cmdlvflptajw.us-east-1.rds.amazonaws.com',
                                    database='team195_scouting')
        self.cursor = self.conn.cursor()
        
        self.connDes = mariaDB.connect(user='admin',
                                    passwd='Einstein195',
                                    host='frcteam195.cmdlvflptajw.us-east-1.rds.amazonaws.com',
                                    database='team195_scouting')

        self.cursorDes = self.connDes.cursor()

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

        self.columns = []
        self._wipeCEA()
        #self._insert()

        print("Time: %0.2f seconds" % (time.time() - start_time))
        print()

    # Function to run a query - the query string must be passed to the function
    def _run_query(self, query):
        self.cursor.execute(query)

    # Function to determine the DB table column headers
    def _setColumns(self, columns):
        self.columns = columns

    # Function to wipe the CEA table. We may want to make this only remove CurrentEvent records.
    def _wipeCEA(self):
        print(CEA_table)
        #self._run_query("DELETE FROM " + CEA_table + ";")
        self._run_query("SELECT * FROM " + CEA_table + ";")
        self.connDes.commit()

    #
    def _insert(self):
        # Insert average data for each team into CurrentEventAnalysisGraphs
        self._run_query("INSERT INTO " + CEA_table + " "
                        "SELECT * FROM " + CEA_table + ";")
        self.connDes.commit()

# This initizlzes the analysis Class and thus runs the program.
if __name__ == '__main__':
    myAnalysis = analysis()