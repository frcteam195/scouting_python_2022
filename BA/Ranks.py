import mariadb as mariaDB
import tbapy
import xlsxwriter
import sys
import getopt
import argparse
import time
import datetime as dt

now = dt.datetime.now()
print(now.strftime("%Y-%m-%d %H:%M:%S"))
start_time = time.time()

database = ''

parser = argparse.ArgumentParser()
parser.add_argument("-db", "--database", help = "Choices: aws-prod, aws-dev, pi-192, pi-10, localhost", required=True)
parser.add_argument("--excel",choices=('True','False'))
args = parser.parse_args()
input_database = args.database
excel = args.excel == 'True'

# print(excel)
# print(input_database)
# sys.exit()

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

tba = tbapy.TBA('Tfr7kbOvWrw0kpnVp5OjeY780ANkzVMyQBZ23xiITUkFo9hWqzOuZVlL3Uy6mLrz')
# x = 195
# team = tba.team(x)



cursor.execute("SELECT Events.BAEventID FROM Events WHERE Events.CurrentEvent = 1;")
event = cursor.fetchone()[0]

eventTeams = tba.event_teams(event)
teamRanks = tba.event_rankings(event).get('rankings')
teamRankList = []

    
if excel == False:
    print("Writing Ranks to database")
    
    cursor.execute("DELETE FROM BlueAllianceRankings")
    cursor.execute("ALTER TABLE BlueAllianceRankings AUTO_INCREMENT = 1;")
    conn.commit()
    
    for teamRank in teamRanks:
        teamRankList.append(teamRank['team_key'][3:])

    for team in teamRankList:
        query = "INSERT INTO BlueAllianceRankings (Team, TeamRank) VALUES " + "('" + str(team) + "', '" + \
                str(teamRankList.index(team) + 1) + "');"
        cursor.execute(query)
        conn.commit()
        
    print("Time: %0.2f seconds" % (time.time() - start_time))
    print()


elif excel == True:
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
    print('Oops, that should not happen')
    sys.exit()
