# use pip3 to install:
# pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

from __future__ import print_function
import os.path
from tokenize import String
import mariadb as mariaDB
import numpy as np
import time
import argparse
import datetime

database = ''
csvFilename = ''
parser = argparse.ArgumentParser()
 
# Adding optional argument
parser.add_argument("-db", "--database", help = "Choices: aws-prod, aws-dev, pi-192, pi-10, localhost", required=True)
 
# Read arguments from command line
args = parser.parse_args()

input_database = args.database
# input_csvFilename = args.csv_filename

if input_database == "aws-prod":
    database = "aws-prod"
elif input_database == "aws-dev":
    database = "aws-dev"
elif input_database == "pi-192":
    database = "pi-192"
elif input_database == "pi-10":
    database = "pi-10"
elif input_database == "localhost":
    database = "localhost"
else:
    print(input_database + " is not a invalid database choice. See --help for choices")
    sys.exit()

print ("Connecting to " + database)

# **************************************************************


# Define a Class called analysis
class analysis():
    def __init__(self):
        now = datetime.datetime.now()
        print(now.strftime("%Y-%m-%d %H:%M:%S"))
        start_time = time.time()
        # Connection to AWS Testing database - use when you would destroy tables with proper data
        if database == "aws-dev":
            print("Input database " + input_database)
            self.conn = mariaDB.connect(user='admin',
                                       passwd='Einstein195',
                                        host='frcteam195testinstance.cmdlvflptajw.us-east-1.rds.amazonaws.com',
                                       database='team195_scouting')
            self.cursor = self.conn.cursor()
        
        # Pi DB with remote access (e.g. from laptop)
        elif database == "pi-10":
            self.conn = mariaDB.connect(user='admin',
                                        passwd='team195',
                                        host='10.0.20.195',
                                        database='team195_scouting')
            self.cursor = self.conn.cursor()
            
        # Pi DB with remote access (e.g. from laptop)
        elif database == "pi-192":
            self.conn = mariaDB.connect(user='admin',
                                        passwd='team195',
                                        host='192.168.1.195',
                                        database='team195_scouting')
            self.cursor = self.conn.cursor()

        # Pi DB with local access (e.g. from the Pi itself)
        elif database == "localhost":
            self.conn = mariaDB.connect(user='admin',
                                        passwd='team195',
                                        host='localhost',
                                        database='team195_scouting')
            self.cursor = self.conn.cursor()

        # Connection to AWS database with proper data
        elif database == "aws-prod":
            self.conn = mariaDB.connect(user='admin',
                                        passwd='Einstein195',
                                        host='frcteam195.cmdlvflptajw.us-east-1.rds.amazonaws.com',
                                        database='team195_scouting')
            self.cursor = self.conn.cursor()

        else:
            print ("oops - that should not happen")
            sys.exit()
        self.columns = []
        self._analyze()

        print("Time: %0.2f seconds" % (time.time() - start_time))
        print()
    def _run_query(self, query):
        self.cursor.execute(query)

    # Function to determine the DB table column headers
    def _setColumns(self, columns):
        self.columns = columns
        
    def _analyze(self):
        self._run_query("SELECT * FROM CurrentEventAnalysis "
                        "WHERE AnalysisTypeID = 1;")
        ceaInfo = self.cursor.fetchall()

        for i in range(len(ceaInfo)):
            team = ceaInfo[i][0]
            startPos = [0, 0, 0, 0, 0, 0]
            startPosID = [1, 2, 3, 4, 5, 6]

            for j in range(12):
                self._run_query(f"SELECT Match{j + 1}Value FROM CurrentEventAnalysis "
                                f"WHERE Team = {team} AND AnalysisTypeID = 1;")
                startInfo = self.cursor.fetchone()

                for k in startInfo:
                    if startInfo[0] != None:
                        startPos[int(k) - 1] += 1
                startPosSort2 = []
                startPosSort2 = sorted(startPos, reverse=True)
                startPosSort = [startPosID for _,startPosID in sorted(zip(startPos,startPosID), reverse=True)]
                #print(f"{startPosSort2}\n{startPosSort}\n")
                curFormat = 16
                for l in range(6):
                    if startPosSort2[l] != 0:
                        self._run_query(f"UPDATE CurrentEventAnalysis "
                                        f"SET Match{startPosSort[l]}Format = {curFormat} "
                                        f"WHERE Team = {team} AND AnalysisTypeID = 1;")
                        self.conn.commit()
                        curFormat -= 1
                    else:
                        self._run_query(f"UPDATE CurrentEventAnalysis "
                                        f"SET Match{startPosSort[l]}Format = 0 "
                                        f"WHERE Team = {team} AND AnalysisTypeID = 1;")
                        self.conn.commit()


if __name__ == '__main__':
    myAnalysis = analysis()