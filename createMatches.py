import mariadb as mariaDB
import sys
import argparse

database = ''
csvFilename = ''
parser = argparse.ArgumentParser()
parser.add_argument("-db", "--database", help = "Choices: aws-prod, aws-dev, pi-192, pi-10, localhost", required=True)
args = parser.parse_args()
input_database = args.database

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

if database == "aws-dev":
        print("Input database " + input_database)
        conn = mariaDB.connect(user='admin',
                                    passwd='xxxx',
                                    host='frcteam195testinstance.cmdlvflptajw.us-east-1.rds.amazonaws.com',
                                    database='team195_scouting')
        cursor = conn.cursor()
        
elif database == "pi-10":
        conn = mariaDB.connect(user='admin',
                                passwd='xxxx',
                                host='10.0.20.195',
                                database='team195_scouting')
        cursor = conn.cursor()
        
elif database == "pi-192":
        conn = mariaDB.connect(user='admin',
                                passwd='xxxx',
                                host='192.168.1.195',
                                database='team195_scouting')
        cursor = conn.cursor()

elif database == "localhost":
        conn = mariaDB.connect(user='admin',
                                passwd='xxxx',
                                host='localhost',
                                database='team195_scouting')
        cursor = conn.cursor()

elif database == "aws-prod":
        conn = mariaDB.connect(user='admin',
                                passwd='xxxx',
                                host='frcteam195.cmdlvflptajw.us-east-1.rds.amazonaws.com',
                                database='team195_scouting')
        cursor = conn.cursor()

else: 
        print ("oops - Harish would not approve of that!")
        sys.exit()


# def wipeBAS():
#         cursor.execute("DELETE FROM BlueAllianceSchedule;")
#         cursor.execute("ALTER TABLE BlueAllianceSchedule AUTO_INCREMENT = 1;")
#         conn.commit()
# wipeBAS()

query = "SELECT Events.EventID, Events.BAEventID FROM Events WHERE Events.CurrentEvent = 1; "
cursor.execute(query)
eventData = cursor.fetchall()
# print(eventData)
eventID = eventData[0][0]
BAEventID = eventData[0][1]
# eventID = [item[0] for item in eventData]
# BAEventID = [item[1] for item in eventData]
# print(eventID)
# print(BAEventID)

query = "SELECT BlueAllianceSchedule.* FROM BlueAllianceSchedule;"
# print(query)
cursor.execute(query)
rsBAMatches = cursor.fetchall()
# print(rsBAMatches[0][7])

if  rsBAMatches[0][7] != BAEventID:
    print("BAEventIDs do not match between BA-Schedule table and Events table")
    quit()

# Find matches from the Matches table and add new records to the MatchScouting table if they do not already exist
for row in rsBAMatches:
    rsMatchRecord = {'EventID': eventID, 'MatchNo': row[0],
                     'RedTeam1': row[1], 'RedTeam2': row[2], 'RedTeam3': row[3],
                     'BlueTeam1': row[4], 'BlueTeam2': row[5], 'BlueTeam3': row[6]}
    # print(rsMatchRecord)
    query = "SELECT COUNT(*) FROM Matches WHERE Matches.MatchNo = " \
            + str(row[0]) + " AND Matches.EventID = " + str(eventID) + ";"
    # print(query)
    cursor.execute(query)
    count = cursor.fetchall()

    # print(count[0][0])
    if count[0][0] == 0:
        items = rsMatchRecord.items()
        columns = str(tuple([x[0] for x in items])).replace("'", "")
        values = str(tuple([x[1] for x in items]))
        cursor.execute("INSERT INTO Matches "
                       + columns + " VALUES "
                       + values + ";")
        conn.commit()
#
#
# # Fix Team #s for the six alliance stations. This is good in case a team number changed or was entered incorrectly
updateQuery = "UPDATE Matches INNER JOIN BlueAllianceSchedule ON (Matches.MatchNo = BlueAllianceSchedule.MatchNo) " \
              "SET Matches.RedTeam1 = BlueAllianceSchedule.RedTeam1, " \
              "Matches.RedTeam2 = BlueAllianceSchedule.RedTeam2, " \
              "Matches.RedTeam3 = BlueAllianceSchedule.RedTeam3, " \
              "Matches.RedTeam1 = BlueAllianceSchedule.RedTeam1, " \
              "Matches.RedTeam2 = BlueAllianceSchedule.RedTeam2, " \
              "Matches.RedTeam3 = BlueAllianceSchedule.RedTeam3 " \
              "WHERE Matches.EventID = " + str(eventID) + " ;"
cursor.execute(updateQuery)
conn.commit()
