import mariadb as mariaDB
import tbapy
import xlsxwriter
import sys
import getopt
import argparse

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
	cursor.execute("DELETE FROM BlueAllianceOPR")
	conn.commit()

	eventTeams = tba.event_teams(event)
	eventOpr = tba.event_oprs(event).get("oprs")
	
	eventOPRSorted = [(k[3:], eventOpr[k]) for k in sorted(eventOpr, key=eventOpr.get, reverse=True)]
	# print(eventOPRSorted)

	for team in eventOPRSorted:
		query = "INSERT INTO BlueAllianceOPR (Team, OPR) VALUES " + "('" + str(team[0]) + "', '" + \
				str(team[1]) + "');"
		print(query)
		cursor.execute(query)
		conn.commit()
	print('Writing OPRs to database')

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
