import mysql.connector as mariaDB

# Pi DB with remote access (e.g. from laptop)
# conn = mariaDB.connect(user='admin',
#                        passwd='team195',
#                        host='10.0.0.195',
#                        database='team195_scouting')
# cursor = conn.cursor()

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

conn = mariaDB.connect(user='admin',
                       passwd='Einstein195',
                       host='frcteam195testinstance.cmdlvflptajw.us-east-1.rds.amazonaws.com',
                       database='team195_scouting')
cursor = conn.cursor()

cursor.execute("DELETE FROM CurrentEventTeams")
conn.commit()


cursor.execute("SELECT BlueAllianceTeams.Team FROM BlueAllianceTeams")
for team in cursor.fetchall():
    query = "INSERT INTO CurrentEventTeams (Team) VALUES (" + team[0] + ");"
    print(query)
    cursor.execute(query)
    conn.commit()
