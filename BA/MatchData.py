# This is a copy of the original Oprs.py file as a starting point.
# Checkout the BlueAlliance API website which will itemize all the possible
#	items that can be pulled and what they are called.

#from asyncio.windows_events import NULL
import mariadb as mariaDB
import tbapy
import xlsxwriter
import sys
import getopt
import argparse
import datetime as dt
import time

now = dt.datetime.now()
print(now.strftime("%Y-%m-%d %H:%M:%S"))
start_time = time.time()

tba = tbapy.TBA('Tfr7kbOvWrw0kpnVp5OjeY780ANkzVMyQBZ23xiITUkFo9hWqzOuZVlL3Uy6mLrz')
# x = 195
# team = tba.team(x)

database = ''

parser = argparse.ArgumentParser()
parser.add_argument("-db", "--database", help = "Choices: aws-prod, aws-dev, pi-192, pi-10, localhost", required=True)
parser.add_argument("--excel",choices=('True','False'))
args = parser.parse_args()
input_database = args.database
excel = args.excel == 'True'

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
                                    passwd='Einstein195',
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
                                passwd='team195',
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
                                passwd='Einstein195',
                                host='frcteam195.cmdlvflptajw.us-east-1.rds.amazonaws.com',
                                database='team195_scouting')
        cursor = conn.cursor()

else: 
        print ("oops - Harish would not approve of that!")
        sys.exit()

cursor.execute("SELECT Events.BAEventID FROM Events WHERE Events.CurrentEvent = 1;")
event = cursor.fetchone()[0]


if excel == False:
    cursor.execute("DELETE FROM BlueAllianceMatchData")
    conn.commit()

    qNum = 0
    eventInfo = tba.event_matches(event)
    
    for match in eventInfo:
        matchInfo = tba.match(match.key)
        matchNum = matchInfo.match_number
        matchTimeRaw = matchInfo.time
        matchActTimeRaw = matchInfo.actual_time
        if matchInfo.actual_time is not None:
            matchTime = dt.datetime.fromtimestamp(matchTimeRaw)
            matchActTime = dt.datetime.fromtimestamp(matchActTimeRaw)

            matchAlliances = matchInfo.alliances
            matchRed = matchAlliances["red"]
            matchBlue = matchAlliances["blue"]

            matchRedTeams = matchRed["team_keys"]
            matchBlueTeams = matchBlue["team_keys"]

            matchRedScore = matchRed["score"]
            matchBlueScore = matchBlue["score"]

            matchBreakdown = match["score_breakdown"]
            matchRedBreakdown = matchBreakdown["red"]
            matchBlueBreakdown = matchBreakdown["blue"]

            matchRedFouls = matchRedBreakdown["foulCount"]
            matchBlueFouls = matchBlueBreakdown["foulCount"]

            matchRedTechFouls = matchRedBreakdown["techFoulCount"]
            matchBlueTechFouls = matchBlueBreakdown["techFoulCount"]

            matchRedAutoPoints = matchRedBreakdown["autoPoints"]
            matchBlueAutoPoints = matchBlueBreakdown["autoPoints"]

            matchRedTelePoints = matchRedBreakdown["teleopPoints"]
            matchBlueTelePoints = matchBlueBreakdown["teleopPoints"]

            matchRedHangarPoints = matchRedBreakdown["endgamePoints"]
            matchBlueHangarPoints = matchBlueBreakdown["endgamePoints"]

            matchRedRankingPoints = matchRedBreakdown["cargoBonusRankingPoint"]
            matchBlueRankingPoints = matchBlueBreakdown["cargoBonusRankingPoint"]

            matchRedHangarRP = matchRedBreakdown["hangarBonusRankingPoint"]
            matchBlueHangarRP = matchBlueBreakdown["hangarBonusRankingPoint"]

            #print(str(matchTime) + "\n")

            if match.comp_level == "qm":
                cursor.execute("INSERT INTO BlueAllianceMatchData(MatchNumber, MatchTime, ActualTime, Red1, Red2, Red3, Blue1, Blue2, Blue3, RedScore, BlueScore, "
                                "RedFouls, BlueFouls, RedTechFouls, BlueTechFouls, RedAutoPoints, BlueAutoPoints, RedTelePoints, BlueTelePoints, "
                                "RedHangerPoints, BlueHangerPoints, RedCargoRanking, BlueCargoRanking, RedHangarRanking, BlueHangarRanking) "
                                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", \
                                (matchNum, str(matchTime)[11:16], str(matchActTime)[11:16], int(str(matchRedTeams[0])[3:]), int(str(matchRedTeams[1])[3:]), int(str(matchRedTeams[2])[3:]), int(str(matchBlueTeams[0])[3:]), int(str(matchBlueTeams[1])[3:]), int(str(matchBlueTeams[2])[3:]), \
                                int(matchRedScore), int(matchBlueScore), int(matchRedFouls), int(matchBlueFouls), int(matchRedTechFouls), int(matchBlueTechFouls), \
                                int(matchRedAutoPoints), int(matchBlueAutoPoints), int(matchRedTelePoints), int(matchBlueTelePoints), int(matchRedHangarPoints), int(matchBlueHangarPoints), \
                                int(matchRedRankingPoints), int(matchBlueRankingPoints), bool(matchRedHangarRP), bool(matchBlueHangarRP)))
                conn.commit()

    print("Time: %0.2f seconds" % (time.time() - start_time))
    print()

	
	#eventInfoSorted = [(k[3:], eventInfo[k]) for k in sorted(eventInfo, key=eventInfo.get, reverse=True)]
	# print(eventOPRSorted)

    #for team in eventInfo:
        #query = "INSERT INTO BlueAllianceOPR (Team, OPR) VALUES " + "('" + str(team[0]) + "', '" + \
                #str(team[1]) + "');"
        # print(query)
        #cursor.execute(query)
        #conn.commit()
        #print(team)
    #print('Writing OPRs to database')

elif excel == True:
	workbook = xlsxwriter.Workbook('OPRS.xlsx')
	worksheet = workbook.add_worksheet()

	row = 0
	col = 0

	eventOpr = tba.event_oprs(event).get("oprs")

	eventOPRSorted = [(k[3:], eventOpr[k]) for k in sorted(eventOpr, key=eventOpr.get, reverse=True)]

	for team in eventOPRSorted:
		worksheet.write_row(row, col, team)
		row += 1

	workbook.close()

else:
	print('Oops, that should not happen')
	sys.exit(0)
