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
        cursor.execute("DELETE FROM BlueAllianceOPR")
        conn.commit()

        eventTeams = tba.event_teams(event)
        eventOpr = tba.event_oprs(event).get("oprs")
        eventOPRSorted = [(k[3:], eventOpr[k]) for k in sorted(eventOpr, key=eventOpr.get, reverse=True)]
        # print(eventOPRSorted)

        for team in eventOPRSorted:
            query = "INSERT INTO BlueAllianceOPR (Team, OPR) VALUES " + "('" + str(team[0]) + "', '" + \
                    str(team[1]) + "');"
            # print(query)
            cursor.execute(query)
            conn.commit()

    elif args == 'excel':
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
        print('The argument needs to be either excel or db')
        sys.exit(0)
