import mysql.connector as mariaDB
import tbapy
import datetime

tba = tbapy.TBA('Tfr7kbOvWrw0kpnVp5OjeY780ANkzVMyQBZ23xiITUkFo9hWqzOuZVlL3Uy6mLrz')
currentYear = datetime.datetime.today().year


def onlyascii(s):
    return "".join(i for i in s if ord(i) < 128 and ord(i) != 39)

conn = mariaDB.connect(user='admin',
                       passwd='Einstein195',
                       host='frcteam195testinstance.cmdlvflptajw.us-east-1.rds.amazonaws.com',
                       database='team195_scouting')
cursor = conn.cursor()

# conn = mariaDB.connect(user='admin',
#                        passwd='Einstein195',
#                        host='frcteam195.cmdlvflptajw.us-east-1.rds.amazonaws.com',
#                        database='team195_scouting')
# cursor = conn.cursor()

totalTeams = tba.teams(year=currentYear)
teamList = []

for team in totalTeams:
    tempNick = ''
    teamNum = team.get('team_number')
    teamCity = str(team.city)
    teamStateProv = str(team.state_prov)
    teamCountry = str(team.country)
    cityState = str(team.city) + ' ' + str(team.state_prov) + ' ' + str(team.country)
    queryLocation = ''
    queryCity = ''
    queryStateProv = ''
    queryCountry = ''
    tempNick = onlyascii(team.nickname)
    if len(tempNick) > 50:
        tempNick = tempNick[:40]
    queryLocation = onlyascii(cityState)
    queryCity = onlyascii(teamCity)
    queryStateProv = onlyascii(teamStateProv)
    queryCountry = onlyascii(teamCountry)
    if len(queryLocation) > 50:
        queryLocation = queryLocation[:40]
    if len(queryCity) > 50:
        queryCity = queryCity[:40]
    if len(queryStateProv) > 50:
        queryStateProv = queryStateProv[:40]
    if len(queryCountry) > 50:
        queryCountry = queryCountry[:40]
    query = "INSERT INTO Teams (Team, TeamName, TeamLocation, TeamCity, TeamStateProv, TeamCountry) VALUES " + \
            "('" + str(teamNum) + \
            "','" + str(tempNick) + \
            "','" + str(queryLocation) + \
            "','" + str(queryCity) + \
            "','" + str(queryStateProv) + \
            "','" + str(queryCountry) + "');"
    print(query)
    cursor.execute(query)
    conn.commit()
