import mysql.connector as mariaDB

# Pi DB with remote access (e.g. from laptop)
# conn = mariaDB.connect(user='admin',
#                        passwd='team195',
#                        host='10.0.0.195',
#                        database='team195_scouting')
# cursor = conn.cursor()

# Pi DB with local access (e.g. from the Pi itself)
# conn = mariaDB.connect(user='admin',
#                        passwd='team195',
#                        host='localhost',
#                        database='team195_scouting')
# cursor = conn.cursor()

# Connection to AWS database with proper data
conn = mariaDB.connect(user='admin',
                       passwd='Einstein195',
                       host='frcteam195.cmdlvflptajw.us-east-1.rds.amazonaws.com',
                       database='team195_scouting')
cursor = conn.cursor()

rankList = []
cursor.execute("SELECT * FROM BlueAllianceRankings")
for team in cursor.fetchall():
    teamDict = {team[0]: team[1]}
    rankList.append(teamDict)
print(rankList)

def ranking(analysis, rsRobotMatches):
    # Initialize the rsCEA record set and define variables specific to this function which lie outside the for loop
    rsCEA = {}
    rsCEA['AnalysisTypeID'] = 200

    for matchResults in rsRobotMatches:
        rsCEA['Team'] = matchResults[analysis.columns.index('Team')]
        rsCEA['EventID'] = matchResults[analysis.columns.index('EventID')]
        autoDidNotShow = matchResults[analysis.columns.index('AutoDidNotShow')]
        scoutingStatus = matchResults[analysis.columns.index('ScoutingStatus')]
        # Skip if DNS or UR
        if autoDidNotShow == 1:
            rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Display'] = ''
        elif scoutingStatus == 2:
            rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Display'] = ''
        else:
            for team in rankList:
                if team == rsCEA['Team']:
                    rsCEA['Match1Display'] = rankList[team]
