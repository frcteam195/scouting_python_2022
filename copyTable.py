import mariadb as mariaDB
import numpy as np
import datetime
import time
import argparse
import sys

# *********************** argument parser **********************

# Initialize parser
destination_database = ''
source_database = ''
table_name = ''
parser = argparse.ArgumentParser()
 
# Adding optional argument
parser.add_argument("-dbs", "--database_source", help = "Choices: aws-prod, aws-dev, pi-192, pi-10, localhost", required=True)
parser.add_argument("-dbd", "--database_destination", help = "Choices: aws-prod, aws-dev, pi-192, pi-10, localhost", required=True)
parser.add_argument("-table", "--table_name", help = "Enter the table name", required=True)

# Read arguments from command line
args = parser.parse_args()

input_source_database = args.database_source
input_destination_database = args.database_destination
table_name = args.table_name

if input_source_database == input_destination_database:
    print("The source and the destination databases must be different")
    sys.exit()

if input_source_database == "aws-prod":
    source_database = "aws-prod"
elif input_source_database == "aws-dev":
    source_database = "aws-dev"
elif input_source_database == "pi-192":
    source_database = "pi-192"
elif input_source_database == "pi-10":
    source_database = "pi-10"
elif input_source_database == "localhost":
    source_database = "localhost"
else:
    print(input_source_database + " is not a invalid source database choice. See --help for choices")
    sys.exit()

print ("Connecting to source database " + source_database)

if input_destination_database == "aws-prod":
    destination_database = "aws-prod"
elif input_destination_database == "aws-dev":
    destination_database = "aws-dev"
elif input_destination_database == "pi-192":
    destination_database = "pi-192"
elif input_destination_database == "pi-10":
    destination_database = "pi-10"
elif input_destination_database == "localhost":
    destination_database = "localhost"
else:
    print(input_destination_database + " is not a invalid destination database choice. See --help for choices")
    sys.exit()

print ("Connecting to destination database " + destination_database)
# **************************************************************


now = datetime.datetime.now()
print(now.strftime("%Y-%m-%d %H:%M:%S"))
start_time = time.time()

if source_database == "aws-dev":
    # Connection to AWS Testing database - use when you would destroy tables with proper data
    connSrc = mariaDB.connect(user='admin',
                                passwd='Einstein195',
                                host='frcteam195testinstance.cmdlvflptajw.us-east-1.rds.amazonaws.com',
                                database='team195_scouting')
    cursorSrc = connSrc.cursor()

elif source_database == "aws-prod":
    connSrc = mariaDB.connect(user='admin',
                                passwd='Einstein195',
                                host='frcteam195.cmdlvflptajw.us-east-1.rds.amazonaws.com',
                                database='team195_scouting')

    cursorSrc = connSrc.cursor()

elif source_database == "pi-10":
    # Pi DB with remote access (e.g. from laptop)
    connSrc = mariaDB.connect(user='admin',
                                passwd='team195',
                                host='10.0.20.195',
                                database='team195_scouting')
    cursorScr = connSrc.cursor()
    
elif source_database == "pi-192":
    connSrc = mariaDB.connect(user='admin',
                                passwd='Einstein195',
                                host='192.168.1.195',
                                port='3306', 
                                database='team195_scouting')
    cursorSrc = connSrc.cursor()

elif source_database == "localhost":
# Pi DB with local access (e.g. from the Pi itself)
    connSrc = mariaDB.connect(user='admin',
                                passwd='team195',
                                host='localhost',
                                database='team195_scouting')
    cursorSrc = connSrc.cursor()

else:
    print("Oops that shouldn't have happened")
    sys.exit()

# *****************************************************************************************

if destination_database == "aws-dev":
    # Connection to AWS Testing database - use when you would destroy tables with proper data
    connDes = mariaDB.connect(user='admin',
                                passwd='Einstein195',
                                host='frcteam195testinstance.cmdlvflptajw.us-east-1.rds.amazonaws.com',
                                database='team195_scouting')
    cursorDes = connDes.cursor()

elif destination_database == "aws-prod":
    connDes = mariaDB.connect(user='admin',
                                passwd='Einstein195',
                                host='frcteam195.cmdlvflptajw.us-east-1.rds.amazonaws.com',
                                database='team195_scouting')

    cursorDes = connDes.cursor()

elif destination_database == "pi-10":
    # Pi DB with remote access (e.g. from laptop)
    connDes = mariaDB.connect(user='admin',
                                passwd='team195',
                                host='10.0.20.195',
                                database='team195_scouting')
    cursorDes = connDes.cursor()
    
elif destination_database == "pi-192":
    connDes = mariaDB.connect(user='admin',
                                passwd='Einstein195',
                                host='192.168.1.195',
                                database='team195_scouting')
    cursorDes = connDes.cursor()

elif destination_database == "localhost":
# Pi DB with local access (e.g. from the Pi itself)
    connDes = mariaDB.connect(user='admin',
                                passwd='team195',
                                host='localhost',
                                database='team195_scouting')
    cursorDes = connDes.cursor()

else:
    print("Oops that shouldn't have happened")
    sys.exit()


def wipeTable():
    cursorDes.execute("DELETE FROM Tmp;")
    cursorDes.execute("ALTER TABLE Tmp AUTO_INCREMENT = 1;")
    connDes.commit()
    print ("Wiping temp table")



columnHeadings=[]
cursorSrc.execute("SELECT * FROM " + table_name + ";")
num_fields = len(cursorSrc.description)
#print(cursorSrc.description)
cursorDes.execute("DROP TABLE IF EXISTS Tmp;")
cursorDes.execute("CREATE TABLE Tmp AS SELECT * FROM " + table_name + ";")
wipeTable()
columnHeadings = str(tuple([i[0] for i in cursorSrc.description])).replace("'", "")
tableContents = cursorSrc.fetchall()
#print(columnHeadings)
#columnHeadings = str(tuple([record[0] for record in tableContents])).replace("'", "")
# print(num_fields)
    
for row in tableContents:
    # print(row)
    valList = list(row)
    row = str(tuple(row))
    # print(valList)
    for j in range(len(valList)):
        if len(str(valList[j])) > 8:
            valList[j] = str(valList[j]).replace("datetime.date(", "")
            valList[j] = str(valList[j]).replace(")", "")
            # print(valList)
            row = str(tuple(valList))
    #print(row)
    query = ("INSERT INTO Tmp " + columnHeadings + " VALUES " + row + ";")
    query = query.replace("None", "NULL")
    # print(query)
    cursorDes.execute(query)
    connDes.commit()
cursorDes.execute("DROP TABLE " + table_name + ";")
cursorDes.execute("ALTER TABLE Tmp RENAME " + table_name + ";")
connDes.commit()
print ("Copying " + table_name + " table complete!")

print("Time: %0.2f seconds" % (time.time() - start_time))
print()

