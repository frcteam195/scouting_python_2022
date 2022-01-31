# Python3 script that pulls all FRC registered teams for the current year and
#	writes the full team list to the Teams table in the Team 195 DB
# Script is intended to be run once at the beginning of the season

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
    tempLocation = ''
    tempCity = ''
    tempStateProv = ''
    tempCountry = ''
    
    teamNum = team.get('team_number')
    cityState = str(team.city) + ' ' + str(team.state_prov) + ' ' + str(team.country)    
    
    tempNick = onlyascii(team.nickname)
    tempLocation = onlyascii(cityState)
    tempCity = onlyascii(team.city)
    tempStateProv = onlyascii(team.state_prov)
    tempCountry = onlyascii(team.country)
    
    if len(tempNick) > 50:
        tempNick = tempNick[:40]
    if len(tempLocation) > 50:
        tempLocation = tempLocation[:40]
    if len(tempCity) > 50:
        tempCity = tempCity[:40]
    if len(tempStateProv) > 50:
        tempStateProv = tempStateProv[:40]
    if len(tempCountry) > 50:
        tempCountry = tempCountry[:40]
    
    query = "INSERT INTO Teams (Team, TeamName, TeamLocation, TeamCity, TeamStateProv, TeamCountry) VALUES " + \
            "('" + str(teamNum) + \
            "','" + str(tempNick) + \
            "','" + str(tempLocation) + \
            "','" + str(tempCity) + \
            "','" + str(tempStateProv) + \
            "','" + str(tempCountry) + "');"
    print(query)
    
    cursor.execute(query)
    conn.commit()
