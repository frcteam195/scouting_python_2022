# Python3 script that pulls all FRC registered teams for the current year and
#	writes the full team list to the Teams table in the Team 195 DB
# Script is intended to be run once at the beginning of the season

import mariadb as mariaDB
import tbapy
import datetime
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

def onlyascii(s):
    return "".join(i for i in s if ord(i) < 128 and ord(i) != 39)

if database == "aws-dev":
        print("Input database " + input_database)
        conn = mariaDB.connect(user='admin',
                                    passwd='RapidReact2022',
                                    host='frcteam195testinstance.cmdlvflptajw.us-east-1.rds.amazonaws.com',
                                    database='team195_scouting')
        cursor = conn.cursor()
        
elif database == "pi-10":
        conn = mariaDB.connect(user='admin',
                                passwd='team195',
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
                                passwd='team195',
                                host='localhost',
                                database='team195_scouting')
        cursor = conn.cursor()

elif database == "aws-prod":
        conn = mariaDB.connect(user='admin',
                                passwd='RapidReact2022',
                                host='frcteam195.cmdlvflptajw.us-east-1.rds.amazonaws.com',
                                database='team195_scouting')
        cursor = conn.cursor()

else: 
        print ("oops - Harish would not approve of that!")
        sys.exit()

tba = tbapy.TBA('Tfr7kbOvWrw0kpnVp5OjeY780ANkzVMyQBZ23xiITUkFo9hWqzOuZVlL3Uy6mLrz')
currentYear = datetime.datetime.today().year

def wipeTTL():
        cursor.execute("DELETE FROM Teams;")
        cursor.execute("ALTER TABLE Teams AUTO_INCREMENT = 1;")
        conn.commit()

wipeTTL()

def onlyascii(s):
    return "".join(i for i in s if ord(i) < 128 and ord(i) != 39)


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
