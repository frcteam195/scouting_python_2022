# Python3 script that pulls all FRC registered teams for the current year and
#	writes the full team list to the Teams table in the Team 195 DB
# Script is intended to be run once at the beginning of the season

import mysql.connector as mariaDB
import tbapy
import datetime
import re
import sys
import argparse

tba = tbapy.TBA('Tfr7kbOvWrw0kpnVp5OjeY780ANkzVMyQBZ23xiITUkFo9hWqzOuZVlL3Uy6mLrz')
currentYear = datetime.datetime.today().year
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

def wipeBAE():
        cursor.execute("DELETE FROM BlueAllianceEvents;")
        cursor.execute("ALTER TABLE BlueAllianceEvents AUTO_INCREMENT = 1;")
        conn.commit()
      

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

else: 
        print ("oops - Harish would not approve of that!")
        sys.exit()

wipeBAE() 
#conn = mariaDB.connect(user='admin',
#                       passwd='Einstein195',
#                       host='frcteam195testinstance.cmdlvflptajw.us-east-1.rds.amazonaws.com',
#                       database='team195_scouting')
#cursor = conn.cursor()

# conn = mariaDB.connect(user='admin',
#                        passwd='Einstein195',
#                        host='frcteam195.cmdlvflptajw.us-east-1.rds.amazonaws.com',
#                        database='team195_scouting')
# cursor = conn.cursor()

totalEvents = tba.events(year=currentYear)
eventList = []

for event in totalEvents:
    eventCode = event.get('event_code')
    eventName = event.get('short_name')
    eventWeek = event.get('week')
    eventCity = event.get('city')
    eventStateProv = event.get('state_prov')
    eventCountry = event.get('country')
    eventLocation = (eventCity + ", " + eventStateProv + ", " + eventCountry)
    eventStartDate = event.get('start_date')
    eventEndDate = event.get('end_date')
    BAEventID = event.get('key')
    
    print (eventCode + " " + eventLocation)
    
    eventName = onlyascii(eventName)
    eventLocation = onlyascii(eventLocation)

    if len(eventName) > 50:
        eventName = eventName[:40]
    if eventName is None:
    	eventName = "no name"
    eventName = re.sub("[{}]","", eventName)
    eventName = re.sub("[()]","", eventName)
    eventLocation = eventLocation.replace("'","")
    if len(eventCity) > 50:
    	eventCity = eventCity[:40]
    if len(eventCountry) > 50:
    	eventCountry = eventCountry[:40]
    if eventWeek is None:
    	eventWeek = 8
    
    
    query = "INSERT INTO BlueAllianceEvents (EventCode, EventName, EventWeek, EventLocation, EventStartDate, EventEndDate, BAEventID) VALUES " + \
            "('" + str(eventCode) + \
            "','" + str(eventName) + \
            "','" + str(eventWeek) + \
            "','" + str(eventLocation) + \
            "','" + str(eventStartDate) + \
            "','" + str(eventEndDate) + \
            "','" + str(BAEventID) + "');"
    print(query)
    
    cursor.execute(query)
    conn.commit()
