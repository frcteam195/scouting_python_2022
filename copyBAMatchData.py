from os import system
import mariadb as mariaDB
import numpy as np
import datetime
import time
import argparse


# *********************** argument parser **********************

# Initialize parser
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

M_table = "Matches"
BAMD_table = "BlueAllianceMatchData"

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
                                       passwd='xxxx',
                                        host='frcteam195testinstance.cmdlvflptajw.us-east-1.rds.amazonaws.com',
                                       database='team195_scouting')
            self.cursor = self.conn.cursor()
        
        # Pi DB with remote access (e.g. from laptop)
        elif database == "pi-10":
            self.conn = mariaDB.connect(user='admin',
                                        passwd='xxxx',
                                        host='10.0.20.195',
                                        database='team195_scouting')
            self.cursor = self.conn.cursor()
            
        # Pi DB with remote access (e.g. from laptop)
        elif database == "pi-192":
            self.conn = mariaDB.connect(user='admin',
                                        passwd='xxxx',
                                        host='192.168.1.195',
                                        database='team195_scouting')
            self.cursor = self.conn.cursor()

        # Pi DB with local access (e.g. from the Pi itself)
        elif database == "localhost":
            self.conn = mariaDB.connect(user='admin',
                                        passwd='xxxx',
                                        host='localhost',
                                        database='team195_scouting')
            self.cursor = self.conn.cursor()

        # Connection to AWS database with proper data
        elif database == "aws-prod":
            self.conn = mariaDB.connect(user='admin',
                                        passwd='xxxx',
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

    # Function to run a query - the query string must be passed to the function
    def _run_query(self, query):
        self.cursor.execute(query)

    # Function to determine the DB table column headers
    def _setColumns(self, columns):
        self.columns = columns

	# Function to write means and medians to the CEAGraphs table
    def _analyze(self):
        self._run_query("SELECT * FROM Events "
                        "WHERE CurrentEvent = 1;")
        eventInfo = self.cursor.fetchone()
        ID = eventInfo[0]

        self._run_query("UPDATE " + M_table + " "
                        "INNER JOIN " + BAMD_table + " ON " + M_table + ".MatchNo = " + BAMD_table + ".MatchNumber "
                        "SET Matches.RedScore = BlueAllianceMatchData.RedScore, Matches.BlueScore = BlueAllianceMatchData.BlueScore, "
                        "Matches.RedFouls = BlueAllianceMatchData.RedFouls, Matches.BlueFouls = BlueAllianceMatchData.BlueFouls, "
                        "Matches.RedTechFouls = BlueAllianceMatchData.RedTechFouls, Matches.BlueTechFouls = BlueAllianceMatchData.BlueTechFouls, "
                        "Matches.RedAutoPoints = BlueAllianceMatchData.RedAutoPoints, Matches.BlueAutoPoints = BlueAllianceMatchData.BlueAutoPoints, "
                        "Matches.RedTelePoints = BlueAllianceMatchData.RedTelePoints, Matches.BlueTelePoints = BlueAllianceMatchData.BlueTelePoints, "
                        "Matches.RedHangarPoints = BlueAllianceMatchData.RedHangerPoints, Matches.BlueHangarPoints = BlueAllianceMatchData.BlueHangerPoints, "
                        "Matches.RedCargoRanking = BlueAllianceMatchData.RedCargoRanking, Matches.BlueCargoRanking = BlueAllianceMatchData.BlueCargoRanking, "
                        "Matches.RedHangarRanking = BlueAllianceMatchData.RedHangarRanking, Matches.BlueHangarRanking = BlueAllianceMatchData.BlueHangarRanking, "
                        "Matches.MatchTime = BlueAllianceMatchData.MatchTime, Matches.ActualTime = BlueAllianceMatchData.ActualTime "
                        "WHERE Matches.EventID = " + str(ID) + ";")
        self.conn.commit()
        

# This initizlzes the analysis Class and thus runs the program.
if __name__ == '__main__':
    myAnalysis = analysis()
