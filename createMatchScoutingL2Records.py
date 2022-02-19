import mysql.connector as mariaDB
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

def wipeML2():
        cursor.execute("DELETE FROM MatchScoutingL2;")
        cursor.execute("ALTER TABLE MatchScoutingL2 AUTO_INCREMENT = 1;")
        conn.commit()
      

def onlyascii(s):
    return "".join(i for i in s if ord(i) < 128 and ord(i) != 39)
if database == "aws-dev":
            print("Input database " + input_database)
            conn = mariaDB.connect(user='admin',
                                       passwd='Einstein195',
                                        host='frcteam195testinstance.cmdlvflptajw.us-east-1.rds.amazonaws.com',
                                       database='team195_scouting')
            cursor = conn.cursor()
        
elif database == "pi-10":
            conn = mariaDB.connect(user='admin',
                                passwd='team195',
                                host='10.0.0.195',
                                database='team195_scouting')
            cursor = conn.cursor()

elif database == "localhost":
        conn = mariaDB.connect(user='admin',
                                passwd='team195',
                                host='localhost',
                                database='team195_scouting')
        cursor = conn.cursor()

elif database == "aws-prod":
        conn = mariaDB.connect(user='admin',
                                passwd='Einstein195',
                                host='frcteam195.cmdlvflptajw.us-east-1.rds.amazonaws.com',
                                database='team195_scouting')
        cursor = conn.cursor()

else: 
        print ("oops - Harish would not approve of that!")
        sys.exit()

wipeML2() 


cursor.execute("SELECT Matches.* FROM Matches LEFT JOIN MatchScoutingL2  "
               "ON (Matches.EventID = MatchScoutingL2.EventID) "
               "AND Matches.MatchID = MatchScoutingL2.MatchID "
               "JOIN Events ON (Events.EventID = Matches.EventID) "
               "WHERE (((Events.CurrentEvent) = 1) AND ((MatchScoutingL2.MatchID) is Null));")
rsMatches = cursor.fetchall()
# print(rsMatches)

# Find matches from the Matches table and add new records to the MatchScoutingL2 table if they do not already exist
for row in rsMatches:
    i = 1
    while i <= 3:
        rsMatchScoutingRecord = {'MatchID': row[0], 'EventID': row[1], 'TeamRed': row[i + 2], 'TeamBlue': row[i + 5], 'AllianceStationID': i+6}
        # print(rsMatchScoutingRecord)
        items = rsMatchScoutingRecord.items()
        columns = str(tuple([x[0] for x in items])).replace("'", "")
        values = str(tuple([x[1] for x in items]))

        query=("INSERT INTO MatchScoutingL2 "
                        + columns + " VALUES "
                        + values + ";")
        print(query)
        cursor.execute(query)
        conn.commit()
        i += 1


# Get MatchEventID's for Red Teams
updateQuery = "UPDATE MatchScoutingL2 " \
              "INNER JOIN MatchScouting on (MatchScoutingL2.TeamRed = MatchScouting.Team) " \
              "INNER JOIN Events on (Events.EventID = MatchScoutingL2.EventID) " \
              "SET MatchScoutingL2.MatchScoutingIDRed=MatchScouting.MatchScoutingID " \
              "WHERE Events.CurrentEvent = 1;"
cursor.execute(updateQuery)
conn.commit()
print(updateQuery)


# Get MatchEventID's for Blue Teams
updateQuery = "UPDATE MatchScoutingL2 " \
              "INNER JOIN MatchScouting on (MatchScoutingL2.TeamBlue = MatchScouting.Team) " \
              "INNER JOIN Events on (Events.EventID = MatchScoutingL2.EventID) " \
              "SET MatchScoutingL2.MatchScoutingIDBlue=MatchScouting.MatchScoutingID " \
              "WHERE Events.CurrentEvent = 1;"
cursor.execute(updateQuery)
conn.commit()
print(updateQuery)

# Fix Red Team #s just in case they change
updateQuery = "UPDATE MatchScoutingL2 " \
              "INNER JOIN MatchScouting on (MatchScoutingL2.MatchScoutingIDRed=MatchScouting.MatchScoutingID) " \
              "INNER JOIN Events on (Events.EventID = MatchScoutingL2.EventID) " \
              "SET MatchScoutingL2.TeamRed = MatchScouting.Team " \
              "WHERE Events.CurrentEvent = 1;"
cursor.execute(updateQuery)
conn.commit()
print(updateQuery)


# Fix Blue Team #s just in case they change
updateQuery = "UPDATE MatchScoutingL2 " \
              "INNER JOIN MatchScouting on (MatchScoutingL2.MatchScoutingIDBlue=MatchScouting.MatchScoutingID) " \
              "INNER JOIN Events on (Events.EventID = MatchScoutingL2.EventID) " \
              "SET MatchScoutingL2.TeamBlue = MatchScouting.Team " \
              "WHERE Events.CurrentEvent = 1;"
cursor.execute(updateQuery)
conn.commit()
print(updateQuery)
