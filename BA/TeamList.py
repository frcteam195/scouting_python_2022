import mysql.connector as mariaDB
import tbapy
import xlsxwriter
import sys
import getopt
tba = tbapy.TBA('Tfr7kbOvWrw0kpnVp5OjeY780ANkzVMyQBZ23xiITUkFo9hWqzOuZVlL3Uy6mLrz')
x = 195
team = tba.team(x)

def sortbyteam(d):
    return d.get('team_number', None)


# Pi DB with remote access (e.g. from laptop)
conn = mariaDB.connect(user='admin',
                       passwd='team195',
                       host='10.0.0.195',
                       database='team195_scouting')
cursor = conn.cursor()
# Amazon devel DB
# conn = mariaDB.connect(user='admin',
#                        passwd='Einstein195',
#                        host='frcteam195.cmdlvflptajw.us-east-1.rds.amazonaws.com',
#                        database='team195_scouting')
# cursor = conn.cursor()

teamList = []
cursor.execute("SELECT Events.BAEventID FROM Events WHERE Events.CurrentEvent = 1;")
event = cursor.fetchone()[0]

print(len(sys.argv))
if len(sys.argv) != 2:
    print('Missing argument [db] or [excel]')
    print('Usage: python3 Schedule.py [db]|[excel]')
    sys.exit(0)
else:
    args = getopt.getopt(sys.argv,"")[1][1]
    if args == 'db':
        cursor.execute("DELETE FROM BlueAllianceTeams")
        conn.commit()

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

    elif args == 'excel':
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


