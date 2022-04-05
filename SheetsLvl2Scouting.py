# use pip3 to install:
# pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

from __future__ import print_function
import os.path
from tokenize import String
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account
import mariadb as mariaDB
import numpy as np
import time
import argparse
import datetime

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'maj.json'
creds = None
creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1_X4YiUqmJCcburZ3smlQqxN1KuXH_DR8Zemk1qIwCpc'

service = build('sheets', 'v4', credentials=creds)

# Call the Sheets API
sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                            range="B2:I999").execute()
values = result.get('values', [])

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

CEAG_table = "SheetsL2Scouting"

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
        self._wipeCEAG()
        self._analyze()

        print("Time: %0.2f seconds" % (time.time() - start_time))
        print()
    def _run_query(self, query):
        self.cursor.execute(query)

    # Function to determine the DB table column headers
    def _setColumns(self, columns):
        self.columns = columns

    # Function to wipe the CEAG table. We may want to make this only remove CurrentEvent records.
    def _wipeCEAG(self):
        self._run_query("DELETE FROM " + CEAG_table + "")
        self.conn.commit()



        
    def _analyze(self):
        for r in range(len(values)):
            self._run_query("INSERT INTO " + CEAG_table + "(Name , MatchNo , TeamNo , OffensiveQualities , DefenseQualities , LabelBot , GeneralThoughts, HarishLove) "
                            "VALUES ('" + values[r][0] +"', "+ values[r][1] +", " + values[r][2] +", '" + values[r][3]+"', '" + values[r][4]+"', '" + values[r][5]+"', '" + values[r][6]+"', '" + values[r][7]+ "')")

            self.conn.commit()
        #print(values)

if __name__ == '__main__':
    myAnalysis = analysis()
