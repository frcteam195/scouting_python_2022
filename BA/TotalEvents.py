# Python3 script that pulls all FRC registered teams for the current year and
#	writes the full team list to the Teams table in the Team 195 DB
# Script is intended to be run once at the beginning of the season

import mysql.connector as mariaDB
import tbapy
import datetime
import re
import sys
tba = tbapy.TBA('Tfr7kbOvWrw0kpnVp5OjeY780ANkzVMyQBZ23xiITUkFo9hWqzOuZVlL3Uy6mLrz')
currentYear = datetime.datetime.today().year

def wipeBAE():
        cursor.execute("DELETE FROM BlueAllianceEvents;")
        conn.commit()
      

def onlyascii(s):
    return "".join(i for i in s if ord(i) < 128 and ord(i) != 39)

conn = mariaDB.connect(user='admin',
                       passwd='Einstein195',
                       host='frcteam195testinstance.cmdlvflptajw.us-east-1.rds.amazonaws.com',
                       database='team195_scouting')
cursor = conn.cursor()
wipeBAE() 
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
