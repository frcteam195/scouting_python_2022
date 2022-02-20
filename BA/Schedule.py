import mysql.connector as mariaDB
import tbapy
import xlsxwriter
import sys
import getopt
import argparse

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
                                host='10.0.0.195',
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

tba = tbapy.TBA('Tfr7kbOvWrw0kpnVp5OjeY780ANkzVMyQBZ23xiITUkFo9hWqzOuZVlL3Uy6mLrz')
#x = 195

def sortbymatch(d):
    return d.get('match_number', None)


#team = tba.team(x)
cursor.execute("SELECT Events.BAEventID FROM Events WHERE Events.CurrentEvent = 1;")
event = str(cursor.fetchone()[0])
print(event)

eventMatchListRed = []
eventMatchListBlue = []
matchNumberList = []
eventMatches = tba.event_matches(event)

    
if excel == False:
	cursor.execute("DELETE FROM BlueAllianceSchedule")
	conn.commit()

	for match in eventMatches:
		if match.comp_level == 'qm':
			matchNumberList.append(match.match_number)
	matchNumberList = sorted(matchNumberList)

	for match in sorted(eventMatches, key=sortbymatch):
		if match.comp_level == 'qm':
			matchNumber = {}
			matchNumber['blue'] = match.alliances.get('blue').get('team_keys')
			matchNumber['blue'] = [key.replace('frc', '') for key in matchNumber['blue']]
			eventMatchListBlue.append(matchNumber)
	# print(eventMatchListBlue)

	for match in sorted(eventMatches, key=sortbymatch):
		if match.comp_level == 'qm':
			matchNumber = {}
			matchNumber['red'] = match.alliances.get('red').get('team_keys')
			matchNumber['red'] = [key.replace('frc', '') for key in matchNumber['red']]
			eventMatchListRed.append(matchNumber)
	# print(eventMatchListRed)

	for match in matchNumberList:
		Red1 = eventMatchListRed[match - 1].get('red')[0]
		Red2 = eventMatchListRed[match - 1].get('red')[1]
		Red3 = eventMatchListRed[match - 1].get('red')[2]
		Blue1 = eventMatchListBlue[match - 1].get('blue')[0]
		Blue2 = eventMatchListBlue[match - 1].get('blue')[1]
		Blue3 = eventMatchListBlue[match - 1].get('blue')[2]
		query = "INSERT INTO BlueAllianceSchedule (MatchNo, RedTeam1, RedTeam2, RedTeam3, " \
				"BlueTeam1, BlueTeam2, BlueTeam3, BAEventsID) VALUES " + \
				"('" + str(match) + "', '" + str(Red1) + "', '" + str(Red2) + "', '" + str(Red3) + "', '" + \
				str(Blue1) + "', '" + str(Blue2) + "', '" + str(Blue3) + "', '" + str(event) + "');"
		print(query)
		cursor.execute(query)
		conn.commit()

elif excel == True:
	workbook = xlsxwriter.Workbook('SCHEDULE.xlsx')
	worksheet = workbook.add_worksheet()

	row = 0
	col = 0
	worksheet.write(col, 0, 'MatchNo')
	worksheet.write(col, 1, 'RedTeam1')
	worksheet.write(col, 2, 'RedTeam2')
	worksheet.write(col, 3, 'RedTeam3')
	worksheet.write(col, 4, 'BlueTeam1')
	worksheet.write(col, 5, 'BlueTeam2')
	worksheet.write(col, 6, 'BlueTeam3')
	worksheet.write(col, 7, 'BAEventID')

	eventMatchList = []
	eventMatches = tba.event_matches(event)

	numberMatch = []
	for match in eventMatches:
		if match.comp_level == 'qm':
			numberMatch.append(match.match_number)

	row = 1
	numberMatch.sort()
	for matches in numberMatch:
		# numberMatch.sort()
		worksheet.write(row, col, matches)
		row += 1

	row = 1
	col = 4
	for match in sorted(eventMatches, key=sortbymatch):
		if match.comp_level == 'qm':
			matchNumber = {}
			matchNumber['blue'] = match.alliances.get('blue').get('team_keys')
			matchNumber['blue'] = [key.replace('frc', '') for key in matchNumber['blue']]
			# if match.comp_level == 'qm':
			eventMatchList.append(matchNumber)
			for key in matchNumber.keys():
				worksheet.write_row(row, col, matchNumber[key])
			row += 1

	row = 1
	col = 1
	for match in sorted(eventMatches, key=sortbymatch):
		if match.comp_level == 'qm':
			matchNumber = {}
			matchNumber['red'] = match.alliances.get('red').get('team_keys')
			matchNumber['red'] = [key.replace('frc', '') for key in matchNumber['red']]
			eventMatchList.append(matchNumber)
			for key in matchNumber.keys():
				worksheet.write_row(row, col, matchNumber[key])
			row += 1

	row = 1
	col = 7
	numberMatch.sort()
	for matches in numberMatch:
		worksheet.write(row, col, event)
		row += 1

	workbook.close()

else:
	print('Oops, that should not happen')
	sys.exit(0)