import mysql.connector as mariaDB
import tbapy
import xlsxwriter
import sys
import getopt
tba = tbapy.TBA('Tfr7kbOvWrw0kpnVp5OjeY780ANkzVMyQBZ23xiITUkFo9hWqzOuZVlL3Uy6mLrz')
x = 195
team = tba.team(x)

# Pi DB with remote access (e.g. from laptop)
# conn = mariaDB.connect(user='admin',
#                        passwd='team195',
#                        host='10.0.0.195',
#                        database='team195_scouting')
# cursor = conn.cursor()
# Amazon devel DB
conn = mariaDB.connect(user='admin',
                       passwd='Einstein195',
                       host='frcteam195.cmdlvflptajw.us-east-1.rds.amazonaws.com',
                       database='team195_scouting')
cursor = conn.cursor()


cursor.execute("DELETE FROM BlueAllianceRankings")
conn.commit()

cursor.execute("SELECT Events.BAEventID FROM Events WHERE Events.CurrentEvent = 1;")
event = cursor.fetchone()[0]

eventTeams = tba.event_teams(event)
teamRanks = tba.event_rankings(event).get('rankings')
teamRankList = []

if len(sys.argv) != 2:
    print('There needs to be one argument that is either excel or db')
    exit(-1)
else:
    args = getopt.getopt(sys.argv,"")[1][1]
    if args == 'db':
        for teamRank in teamRanks:
            teamRankList.append(teamRank['team_key'][3:])

        for team in teamRankList:
            query = "INSERT INTO BlueAllianceRankings (Team, TeamRank) VALUES " + "('" + str(team) + "', '" + \
                    str(teamRankList.index(team) + 1) + "');"
            cursor.execute(query)
            conn.commit()

    elif args == 'excel':
        workbook = xlsxwriter.Workbook('EVENT RANKINGS.xlsx')
        worksheet = workbook.add_worksheet()

        row = 0
        col = 0

        matchesPlayed = tba.event_rankings(event).get('rankings')
        matchesPlayedDict = {}
        for team in matchesPlayed:
            matchesPlayedDict[team.get("rank")] = team.get("matches_played")

        row = 1
        col = 2
        for key in matchesPlayedDict.keys():
            worksheet.write(row, col, matchesPlayedDict[key])
            row += 1

        teamRanks = tba.event_rankings(event).get('rankings')
        teamRankDict = {}
        for rank in teamRanks:
            teamRankDict[rank.get("rank")] = rank.get("team_key")[3:]

        row = 1
        col = 0
        for key in teamRankDict.keys():
            worksheet.write(row, col, key)
            worksheet.write(row, col + 1, teamRankDict[key])
            row += 1

        quals = tba.event_rankings(event).get('rankings')
        qualAverage = {}
        for team in quals:
            qualAverage[team.get("rank")] = team.get("qual_average")

        row = 1
        col = 3
        for key in qualAverage.keys():
            worksheet.write(row, col, qualAverage[key])
            row += 1

        workbook.close()

    else:
        print('The argument needs to be either excel or db')
        exit(-1)