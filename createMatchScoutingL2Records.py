import mysql.connector as mariaDB

# Pi DB with remote access (e.g. from laptop)
conn = mariaDB.connect(user='admin',
                       passwd='team195',
                       host='10.0.0.195',
                       database='team195_scouting')
cursor = conn.cursor()

# Pi DB with local access (e.g. from the Pi itself)
# conn = mariaDB.connect(user='admin',
#                        passwd='team195',
#                        host='localhost',
#                        database='team195_scouting')
# cursor = conn.cursor()

# Connection to AWS database with proper data
# conn = mariaDB.connect(user='admin',
#                        passwd='Einstein195',
#                        host='frcteam195.cmdlvflptajw.us-east-1.rds.amazonaws.com',
#                        database='team195_scouting')
# cursor = conn.cursor()


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
