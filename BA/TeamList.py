import mysql.connector as mariaDB
import tbapy
import xlsxwriter
import sys
import getopt
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
elif input_database == "excel":
    database = "excel"
else:
    print(input_database + " is not a invalid database choice. See --help for choices")
    sys.exit()

print ("Connecting to " + database)      

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
elif database == "excel":
    ""
else: 
        print ("oops - Harish would not approve of that!")
        sys.exit()

tba = tbapy.TBA('Tfr7kbOvWrw0kpnVp5OjeY780ANkzVMyQBZ23xiITUkFo9hWqzOuZVlL3Uy6mLrz')
x = 195
team = tba.team(x)

def sortbyteam(d):
    return d.get('team_number', None)


def wipeBAT():
        cursor.execute("DELETE FROM BlueAllianceTeams;")
        cursor.execute("ALTER TABLE BlueAllianceTeams AUTO_INCREMENT = 1;")
        conn.commit()

teamList = []
cursor.execute("SELECT Events.BAEventID FROM Events WHERE Events.CurrentEvent = 1;")
event = cursor.fetchone()[0]

print(len(sys.argv))
if len(sys.argv) != 2:
    print('Missing argument [db] or [excel]')
    print('Usage: python3 Schedule.py [db]|[excel]')
    sys.exit(0)
else:
    
    if database == "aws-dev" or database == "aws-prod" or database == "ai-10" or database == "localhost":
        wipeBAT()

        eventTeams = tba.event_teams(event)
        for team in sorted(eventTeams, key=sortbyteam):
            tempNick = ''
            cityState = str(team.city) + ' ' + str(team.state_prov) + ' ' + str(team.country)
            teams = [team.team_number, team.nickname, cityState]
            teamList.append(teams)
            for char in team.nickname:
                if char.isalnum() or char == ' ':
                    tempNick += char
            values = "(" + str(team.team_number) + "," + team.nickname + "," + cityState + ")"
            query = "INSERT INTO BlueAllianceTeams (Team, TeamName, TeamLocation) VALUES " + "('" + str(team.team_number) + \
                     "','" + tempNick + "','" + str(cityState) + "');"
            # print(query)

            cursor.execute(query)
            conn.commit()

    elif database == 'excel':
        workbook = xlsxwriter.Workbook('TEAM LIST.xlsx')
        worksheet = workbook.add_worksheet()

        row = 0
        col = 0

        worksheet.write(col, 0, 'Team')
        worksheet.write(col, 1, 'TeamName')
        worksheet.write(col, 2, 'TeamLocation')

        row = 1
        eventTeams = tba.event_teams(event)
        teamList = []
        for team in sorted(eventTeams, key=sortbyteam):
            cityState = str(team.city) + ', ' + str(team.state_prov) + ' ' + str(team.country)
            tempTeamsList = [team.team_number, team.nickname, cityState]
            teamList.append(tempTeamsList)
            for teamData in teamList:
                for tempTeam in tempTeamsList:
                    worksheet.write_row(row, col, tempTeamsList)
            row += 1
        row = 1
        # print(teamList)
        workbook.close()

    else:
        print('The argument needs to be either excel or db')
        sys.exit(0)


