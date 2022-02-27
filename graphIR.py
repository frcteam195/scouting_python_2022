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

CEAG_table = "CurrentEventAnalysisGraphs"

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
                                        host='10.0.0.195',
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
        self._wipeCEAG()
        self._analyze()

        print("Time: %0.2f seconds" % (time.time() - start_time))
        print()

    # Function to run a query - the query string must be passed to the function
    def _run_query(self, query):
        self.cursor.execute(query)

    # Function to determine the DB table column headers
    def _setColumns(self, columns):
        self.columns = columns

    # Function to wipe the CEAG table. We may want to make this only remove CurrentEvent records.
    def _wipeCEAG(self):
        self._run_query("DELETE FROM " + CEAG_table + "")
        self.conn.commit()

	# Function to write means and medians to the CEAGraphs table
    def _analyze(self):
        analysisTypeList = [60, 61, 30, 20, 21, 22, 11, 62]
        analysisNameList = ["TotalBallsMean", "TotalScoreMean", "ClimbMean", "TeleLowBallsMean", "TeleHighBallsMean", "TeleTotalBallsMean", "AutonomousScoreMean", "TeleBallScoreMean", "TotalBallsMedian", "TotalScoreMedian", "ClimbMedian", "TeleLowBallsMedian", "TeleHighBallsMedian", "TeleTotalBallsMedian", "AutonomousScoreMedian", "TeleBallScoreMedian"]
        self._run_query("INSERT INTO " + CEAG_table + "(Team, EventID, AutonomousMean, AutonomousMedian) "
                            "SELECT Team, EventID, Summary1Value, Summary2Value "
                            "FROM CurrentEventAnalysis "
                            "WHERE AnalysisTypeID = 10;")
        for i in range(len(analysisTypeList)):
            #print(i)
            self._run_query("UPDATE " + CEAG_table + " "
                            "INNER JOIN CurrentEventAnalysis ON " + CEAG_table + ".Team = CurrentEventAnalysis.Team AND " + CEAG_table + ".EventID = CurrentEventAnalysis.EventID "
                            "SET " + analysisNameList[i] + " = CurrentEventAnalysis.Summary1Value, " + analysisNameList[i + 8] + " = CurrentEventAnalysis.Summary2Value "
                            "WHERE CurrentEventAnalysis.AnalysisTypeID = " + str(analysisTypeList[i]) + ";")
        self.conn.commit()

# This initizlzes the analysis Class and thus runs the program.
if __name__ == '__main__':
    myAnalysis = analysis()
