import mariadb as mariaDB
import argparse

database = ''

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

# def wipeMSR():
#         cursor.execute("DELETE FROM MatchScouting;")
#         cursor.execute("ALTER TABLE MatchScouting AUTO_INCREMENT = 1;")
#         conn.commit()
# wipeMSR()


cursor.execute("SELECT Matches.* FROM Matches LEFT JOIN MatchScouting "
               "ON (Matches.EventID = MatchScouting.EventID) "
               "AND Matches.MatchID = MatchScouting.MatchID "
               "JOIN Events ON (Events.EventID = Matches.EventID) "
               "WHERE (((Events.CurrentEvent) = 1) AND ((MatchScouting.MatchID) is Null));")
rsMatches = cursor.fetchall()
# cursor.execute("SELECT Matches.* FROM Matches "
#                "JOIN Events ON (Events.EventID = Matches.EventID) "
#                "WHERE ((Events.CurrentEvent) = 1) ;")
# rsMatches = cursor.fetchall()
print(rsMatches)

# Find matches from the Matches table and add new records to the MatchScouting table if they do not already exist
for row in rsMatches:
    i = 1
    while i <= 6:
        rsMatchScoutingRecord = {'MatchID': row[0], 'EventID': row[1], 'Team': row[i + 2], 'AllianceStationID': str(i)}
        print(rsMatchScoutingRecord)
        items = rsMatchScoutingRecord.items()
        columns = str(tuple([x[0] for x in items])).replace("'", "")
        values = str(tuple([x[1] for x in items]))
        print(columns)
        print(values)
        cursor.execute("INSERT INTO MatchScouting "
                       + columns + " VALUES "
                       + values + ";")
        conn.commit()
        i += 1


# Fix Team #s for the six alliance stations. This is good in case a team number changed or was entered incorrectly
updateQuery = "UPDATE MatchScouting INNER JOIN Matches ON (MatchScouting.MatchID = Matches.MatchID) " \
              "INNER JOIN Events ON (Events.EventID = Matches.EventID) " \
              "SET MatchScouting.Team = Matches.RedTeam1 " \
              "WHERE Events.CurrentEvent = 1 AND MatchScouting.AllianceStationID = 1"
cursor.execute(updateQuery)
conn.commit()

updateQuery = "UPDATE MatchScouting INNER JOIN Matches ON (MatchScouting.MatchID = Matches.MatchID) " \
              "INNER JOIN Events ON (Events.EventID = Matches.EventID) " \
              "SET MatchScouting.Team = Matches.RedTeam2 " \
              "WHERE Events.CurrentEvent = 1 AND MatchScouting.AllianceStationID = 2"
cursor.execute(updateQuery)
conn.commit()

updateQuery = "UPDATE MatchScouting INNER JOIN Matches ON (MatchScouting.MatchID = Matches.MatchID) " \
              "INNER JOIN Events ON (Events.EventID = Matches.EventID) " \
              "SET MatchScouting.Team = Matches.RedTeam3 " \
              "WHERE Events.CurrentEvent = 1 AND MatchScouting.AllianceStationID = 3"
cursor.execute(updateQuery)
conn.commit()

updateQuery = "UPDATE MatchScouting INNER JOIN Matches ON (MatchScouting.MatchID = Matches.MatchID) " \
              "INNER JOIN Events ON (Events.EventID = Matches.EventID) " \
              "SET MatchScouting.Team = Matches.BlueTeam1 " \
              "WHERE Events.CurrentEvent = 1 AND MatchScouting.AllianceStationID = 4"
cursor.execute(updateQuery)
conn.commit()

updateQuery = "UPDATE MatchScouting INNER JOIN Matches ON (MatchScouting.MatchID = Matches.MatchID) " \
              "INNER JOIN Events ON (Events.EventID = Matches.EventID) " \
              "SET MatchScouting.Team = Matches.BlueTeam2 " \
              "WHERE Events.CurrentEvent = 1 AND MatchScouting.AllianceStationID = 5"
cursor.execute(updateQuery)
conn.commit()

updateQuery = "UPDATE MatchScouting INNER JOIN Matches ON (MatchScouting.MatchID = Matches.MatchID) " \
              "INNER JOIN Events ON (Events.EventID = Matches.EventID) " \
              "SET MatchScouting.Team = Matches.BlueTeam3 " \
              "WHERE Events.CurrentEvent = 1 AND MatchScouting.AllianceStationID = 6"
cursor.execute(updateQuery)
conn.commit()


# add team match numbers by looping back through each teams matches and counting
cursor.execute("SELECT DISTINCT MatchScouting.Team "
               "FROM MatchScouting INNER JOIN Events ON MatchScouting.EventID = Events.EventID "
               "AND ((Events.CurrentEvent) = 1) "
               "ORDER BY MatchScouting.Team; ")
rsTeams = cursor.fetchall()
# print(rsTeams)

for team in rsTeams:
    # print(team[0])
    cursor.execute("SELECT MatchScouting.MatchScoutingID FROM MatchScouting INNER JOIN Events "
                   "ON MatchScouting.EventID = Events.EventID AND ((Events.CurrentEvent) = 1) "
                   "WHERE MatchScouting.Team = "
                   + team[0] + " ORDER BY MatchScouting.MatchScoutingID; ")
    rsTeamMatchScouting = cursor.fetchall()
    # print(rsTeamMatchScouting)
    matchNum = 0
    for match in rsTeamMatchScouting:
        matchNum += 1
        # print(match[0])
        query = "UPDATE MatchScouting SET MatchScouting.TeamMatchNo = " + str(matchNum) + " WHERE MatchScouting.MatchScoutingID = " + str(match[0]) + ";"
        # print(query)
        cursor.execute(query)
        conn.commit()
