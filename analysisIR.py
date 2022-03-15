
import mariadb as mariaDB
import numpy as np
import datetime
import time
import argparse
import sys

# For each analysisType we create add a new import statement. We could import all analysisTypes
# Pre match 1-9
from analysisTypes.startingPosition import startingPosition  #1
from analysisTypes.autoPickup import autoPickup  #2
from analysisTypes.driveStation import driveStation  #2
# auto 10-19
from analysisTypes.autonomous import autonomous  #10
from analysisTypes.autonomousScore import autonomousScore  #11
from analysisTypes.autoLowBalls import autoLowBalls #12
from analysisTypes.autoHighBalls import autoHighBalls #13
# tele 20-29
from analysisTypes.teleLowBalls import teleLowBalls   #20
from analysisTypes.teleHighBalls import teleHighBalls   #21
from analysisTypes.teleTotalBalls import teleTotalBalls   #22
# climb 30-39
from analysisTypes.climb import climb   #30
# summary data 40-59
from analysisTypes.summGroundPickup import summGroundPickup   #40
from analysisTypes.summDefPlayedAgainst import summDefPlayedAgainst   #41
from analysisTypes.summLaunchPad import summLaunchPad   #42
from analysisTypes.summSortCargo import summSortCargo    #43
from analysisTypes.summShootDriving import summShootDriving   #44
from analysisTypes.summTerminalPickup import summTerminalPickup   #45
from analysisTypes.summPlayedDefense import summPlayedDefense   #46
from analysisTypes.summLostComm import summLostComm   #47
from analysisTypes.summSubSystemBroke import summSubSystemBroke   #48
from analysisTypes.summBrokeDown import summBrokeDown   #49
# Totals 60-69
from analysisTypes.totalBalls import totalBalls   #60
from analysisTypes.totalScore import totalScore   #61
from analysisTypes.teleBallScore import teleBallScore   #62
from analysisTypes.matchVideos import matchVideos #70
from analysisTypes.scouter import scouter #71

# *********************** argument parser **********************

# Initialize parser
database = ''
csvFilename = ''
parser = argparse.ArgumentParser()
 
# Adding optional argument
parser.add_argument("-db", "--database", help = "Choices: aws-prod, aws-dev, pi-192, pi-10, localhost", required=True)
# parser.add_argument("-cf", "--csv_filename", help = "Enter the filename for CSV file output", required=True)
 
# Read arguments from command line
args = parser.parse_args()

input_database = args.database
# input_csvFilename = args.csv_filename

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

# **************************************************************

CEA_table = "CurrentEventAnalysisTmp"
BAO_table = "BlueAllianceOPR"
BAR_table = "BlueAllianceRankings"
MS_table = "MatchScouting"

# Define a Class called analysis
class analysis():
    # Inside the class there are several functions defined _run_query, _setColumns, _wipeCEA, _getTeams,
    #   _getTeamData, _analyzeTeams, and _insertAnalysis. Those functions will not get called automatically
    #   so in order to get them to run we create a __init__ function which is a special function in Python
    #   that gets run every time the Class is initialized. Here we build the DB connection cursor from within
    #   the __init__ function and then call the cursor, columns, wipeCEA, rsRobots, and analyzeTeams functions
    #   from within the __init__ function, which means they will be run automatically when the Class is initialized
    def __init__(self):
        now = datetime.datetime.now()
        print(now.strftime("%Y-%m-%d %H:%M:%S"))
        start_time = time.time()
        
        # Connection to AWS Testing database - use when you would destroy tables with proper data
        if database == "aws-dev":
            print("Input database " + input_database)
            self.conn = mariaDB.connect(user='admin',
                                       passwd='Einstein195',
                                        host='frcteam195testinstance.cmdlvflptajw.us-east-1.rds.amazonaws.com',
                                       database='team195_scouting')
            self.cursor = self.conn.cursor()
        
        # Pi DB with remote access (e.g. from laptop)
        elif database == "pi-10":
            self.conn = mariaDB.connect(user='admin',
                                        passwd='team195',
                                        host='10.0.20.195',
                                        database='team195_scouting')
            self.cursor = self.conn.cursor()
            
        # Pi DB with remote access (e.g. from laptop)
        elif database == "pi-192":
            self.conn = mariaDB.connect(user='admin',
                                        passwd='team195',
                                        host='192.168.1.195',
                                        database='team195_scouting')
            self.cursor = self.conn.cursor()

        # Pi DB with local access (e.g. from the Pi itself)
        elif database == "localhost":
            self.conn = mariaDB.connect(user='admin',
                                        passwd='team195',
                                        host='localhost',
                                        database='team195_scouting')
            self.cursor = self.conn.cursor()

        # Connection to AWS database with proper data
        elif database == "aws-prod":
            self.conn = mariaDB.connect(user='admin',
                                        passwd='Einstein195',
                                        host='frcteam195.cmdlvflptajw.us-east-1.rds.amazonaws.com',
                                        database='team195_scouting')
            self.cursor = self.conn.cursor()

        else:
            print ("oops - that should not happen")
            sys.exit()

        self._createTemp()
        self.columns = []
        self._wipeCEA()
        self.rsRobots = self._getTeams()
        self._analyzeTeams()
        self._rankTeamsAll()
        self._renameTable()

        print("Time: %0.2f seconds" % (time.time() - start_time))
        print()

    # Function to run a query - the query string must be passed to the function
    def _run_query(self, query):
        self.cursor.execute(query)

    # Function to determine the DB table column headers
    def _setColumns(self, columns):
        self.columns = columns

    # Function to wipe the CEA table. We may want to make this only remove CurrentEvent records.
    def _wipeCEA(self):
        self._run_query("DELETE FROM " + CEA_table + ";")
        self.conn.commit()

    def _wipeCEA(self):
        self._run_query("DELETE FROM " + CEA_table + ";")
        self.conn.commit()

    def _createTemp(self):
        self._run_query("DROP TABLE IF EXISTS CurrentEventAnalysisTmp;")
        self._run_query("CREATE TABLE CurrentEventAnalysisTmp ("
        "Team VARCHAR(10) NULL, "
        "AnalysisTypeID INT NULL, "
        "EventID INT NULL, "
        "Match1Display VARCHAR(10) NULL, "
        "Match1Format INT NULL, "
        "Match1Value FLOAT NULL, "
        "Match2Display VARCHAR(10) NULL, "
        "Match2Format INT NULL, "
        "Match2Value FLOAT NULL, "
        "Match3Display VARCHAR(10) NULL, " 
        "Match3Format INT NULL, "
        "Match3Value FLOAT NULL, "
        "Match4Display VARCHAR(10) NULL, " 
        "Match4Format INT NULL, "
        "Match4Value FLOAT NULL, "
        "Match5Display VARCHAR(10) NULL, " 
        "Match5Format INT NULL, "
        "Match5Value FLOAT NULL, "
        "Match6Display VARCHAR(10) NULL, " 
        "Match6Format INT NULL, "
        "Match6Value FLOAT NULL, "
        "Match7Display VARCHAR(10) NULL, " 
        "Match7Format INT NULL, "
        "Match7Value FLOAT NULL, "
        "Match8Display VARCHAR(10) NULL, " 
        "Match8Format INT NULL, "
        "Match8Value FLOAT NULL, "
        "Match9Display VARCHAR(10) NULL, " 
        "Match9Format INT NULL, "
        "Match9Value FLOAT NULL, "
        "Match10Display VARCHAR(10) NULL, " 
        "Match10Format INT NULL, "
        "Match10Value FLOAT NULL, "
        "Match11Display VARCHAR(10) NULL, " 
        "Match11Format INT NULL, "
        "Match11Value FLOAT NULL, "
        "Match12Display VARCHAR(10) NULL, " 
        "Match12Format INT NULL, "
        "Match12Value FLOAT NULL, "
        "Summary1Display VARCHAR(10) NULL, " 
        "Summary1Format INT NULL, "
        "Summary1Value FLOAT NULL, "
        "Summary2Display VARCHAR(10) NULL, " 
        "Summary2Format INT NULL, "
        "Summary2Value FLOAT NULL, "
        "Summary3Display VARCHAR(10) NULL, " 
        "Summary3Format INT NULL, "
        "Summary3Value FLOAT NULL, "
        "Summary4Display VARCHAR(10) NULL, " 
        "Summary4Format INT NULL, "
        "Summary4Value FLOAT NULL, "
        "Minimum FLOAT NULL, "
        "Maximum FLOAT NULL, "
        "Percent FLOAT NULL)")

    def _renameTable(self):
        self._run_query("DROP TABLE CurrentEventAnalysis;")
        self._run_query("ALTER TABLE " + CEA_table + " RENAME CurrentEventAnalysis;")
        self.conn.commit()

    # Function to get the team list and set it to rsRobots. Uses the _run_query function defined above.
    #   The assert statement will return rsRobots if the record length > 0 and will exit with the
    #       message "No robots founds" if the record length is 0.
    def _getTeams(self):
        self._run_query("SELECT MatchScouting.Team FROM (MatchScouting "
                       "INNER JOIN Matches ON MatchScouting.MatchID = Matches.MatchID) "
                       "INNER JOIN Events ON Matches.EventID = Events.EventID "
                       "WHERE (((Events.CurrentEvent) = 1)) "
                       "GROUP BY CAST(MatchScouting.Team AS INT), MatchScouting.Team "
                       "HAVING (((MatchScouting.Team) Is Not Null)); ")
        rsRobots = self.cursor.fetchall()

        assert len(rsRobots) > 0, "No robots found"
        return rsRobots

    # Function to retrieve data records for a given team for all their matches and set it to rsRobotMatches
    def _getTeamData(self, team):
        self._run_query("SELECT MatchScouting.*, Matches.MatchNo, Teams.RobotWeight "
            "FROM (Events INNER JOIN Matches ON Events.EventID = Matches.EventID) "
            "INNER JOIN MatchScouting ON (Matches.EventID = MatchScouting.EventID) "
            "AND (Matches.MatchID = MatchScouting.MatchID) "
            "INNER JOIN Teams ON (MatchScouting.Team = Teams.Team) "
            "WHERE (((MatchScouting.Team) = " + team[0] + " "
            "AND ((Events.CurrentEvent) = 1))"
            "AND ((ScoutingStatus = 1) Or (ScoutingStatus = 2) Or (ScoutingStatus = 3)) "
            "AND (MatchScouting.TeamMatchNo <= 12)) "
            "ORDER BY MatchScouting.TeamMatchNo;")

        # Set columns to be a list of column headings in the Query results
        # Very cool - cursor.description is used to auto-determine the column headings in the MatchScouting table
        #   so these values do not need to be hard-coded
        self._setColumns([column[0] for column in list(self.cursor.description)])

        rsRobotMatches = self.cursor.fetchall()

        # If rsRobotMatches is not zero length return rsRobotMatches otherwise return None. This allows the
        #   function to skip a robot analysis if that robot does not have any match records yet.
        if rsRobotMatches:
            return rsRobotMatches
        else:
            return None

    #
    def _analyzeTeams(self):
        # Loop over the # of teams and run each of the analysis functions calling _insertAnalysis after each one is run
        for team in self.rsRobots:
            # print(team)
            rsRobotMatches = self._getTeamData(team)
            teamName = str(team)
            teamName = teamName.replace("('", "")
            teamName = teamName.replace("',)", "")
            # print(rsRobotMatches)

            if rsRobotMatches:
                rsCEA = startingPosition(analysis=self, rsRobotMatches=rsRobotMatches)
                self._insertAnalysis(rsCEA)

                rsCEA = autoPickup(analysis=self, rsRobotMatches=rsRobotMatches)
                self._insertAnalysis(rsCEA)
                
                rsCEA = autonomous(analysis=self, rsRobotMatches=rsRobotMatches)
                self._insertAnalysis(rsCEA)
                
                rsCEA = autonomousScore(analysis=self, rsRobotMatches=rsRobotMatches)
                self._insertAnalysis(rsCEA)

                rsCEA = autoLowBalls(analysis=self, rsRobotMatches=rsRobotMatches)
                self._insertAnalysis(rsCEA)

                rsCEA = autoHighBalls(analysis=self, rsRobotMatches=rsRobotMatches)
                self._insertAnalysis(rsCEA)

                rsCEA = teleLowBalls(analysis=self, rsRobotMatches=rsRobotMatches)
                self._insertAnalysis(rsCEA)
                
                rsCEA = teleHighBalls(analysis=self, rsRobotMatches=rsRobotMatches)
                self._insertAnalysis(rsCEA)
                
                rsCEA = teleTotalBalls(analysis=self, rsRobotMatches=rsRobotMatches)
                self._insertAnalysis(rsCEA)
                
                rsCEA = climb(analysis=self, rsRobotMatches=rsRobotMatches)
                self._insertAnalysis(rsCEA)
                
                rsCEA = summGroundPickup(analysis=self, rsRobotMatches=rsRobotMatches)
                self._insertAnalysis(rsCEA)
                
                rsCEA = summDefPlayedAgainst(analysis=self, rsRobotMatches=rsRobotMatches)
                self._insertAnalysis(rsCEA)
                
                rsCEA = summLaunchPad(analysis=self, rsRobotMatches=rsRobotMatches)
                self._insertAnalysis(rsCEA)
                
                rsCEA = summSortCargo(analysis=self, rsRobotMatches=rsRobotMatches)
                self._insertAnalysis(rsCEA)
                
                rsCEA = summShootDriving(analysis=self, rsRobotMatches=rsRobotMatches)
                self._insertAnalysis(rsCEA)
                
                rsCEA = summTerminalPickup(analysis=self, rsRobotMatches=rsRobotMatches)
                self._insertAnalysis(rsCEA)
                
                rsCEA = summPlayedDefense(analysis=self, rsRobotMatches=rsRobotMatches)
                self._insertAnalysis(rsCEA)
                
                rsCEA = summLostComm(analysis=self, rsRobotMatches=rsRobotMatches)
                self._insertAnalysis(rsCEA)
                
                rsCEA = summSubSystemBroke(analysis=self, rsRobotMatches=rsRobotMatches)
                self._insertAnalysis(rsCEA)
                
                rsCEA = summBrokeDown(analysis=self, rsRobotMatches=rsRobotMatches)
                self._insertAnalysis(rsCEA)
                
                rsCEA = totalBalls(analysis=self, rsRobotMatches=rsRobotMatches)
                self._insertAnalysis(rsCEA)
                
                rsCEA = totalScore(analysis=self, rsRobotMatches=rsRobotMatches)
                self._insertAnalysis(rsCEA)
                
                rsCEA = teleBallScore(analysis=self, rsRobotMatches=rsRobotMatches)
                self._insertAnalysis(rsCEA)
                
                rsCEA = matchVideos(analysis=self, rsRobotMatches=rsRobotMatches)
                self._insertAnalysis(rsCEA)
                
                rsCEA = scouter(analysis=self, rsRobotMatches=rsRobotMatches)
                self._insertAnalysis(rsCEA)
                
                rsCEA = driveStation(analysis=self, rsRobotMatches=rsRobotMatches)
                self._insertAnalysis(rsCEA)


                self._run_query("INSERT INTO " + CEA_table + "(Team, Summary1Value, Summary1Display, Summary2Value, Summary2Display, AnalysisTypeID) "
                                "SELECT " + BAR_table + ".Team, OPR, OPR, TeamRank, TeamRank, 80 "
                                "FROM " + BAR_table + " "
                                "INNER JOIN " + BAO_table + " ON " + BAR_table + ".Team = " + BAO_table + ".Team "
                                "WHERE " + BAR_table + ".Team = " + teamName + ";")

                self._run_query("UPDATE " + CEA_table + " "
                                "INNER JOIN " + MS_table + " ON " + CEA_table + ".Team = " + MS_table + ".Team "
                                "SET " + CEA_table + ".EventID = " + MS_table + ".EventID "
                                "WHERE " + MS_table + ".Team = " + teamName + " AND AnalysisTypeID = 80;")

                self.conn.commit()

    # Helper function to rank a single analysis type, called by _rankTeamsAll
    def _rankTeamsSingle(self, analysis_type):
        # Get Summary 1 value for each team from CEA with analysis_type
        # Sort in descending order by sum 1 value
        # Determine percentile of each team
        # Optional: see if at percentile cutoffs there is any repeated values
        # Update summary 3 value in CEA for each team (rank based on percentile)
        self._run_query("SELECT Team, Summary1Value "
                        "FROM " + CEA_table + " "
                        "WHERE AnalysisTypeID = " + str(analysis_type) + ";")
        team_sum1 = self.cursor.fetchall() # List of tuples (team, summary1value)
        if len(team_sum1) > 0:
            team_sum1 = [team_tup for team_tup in team_sum1 if team_tup[1] is not None]
            # print(team_sum1)
            sum1 = [item[1] for item in team_sum1]
            percentiles = np.percentile(sum1, [25, 50, 75, 90])

            team_coloring = {}
            for team in team_sum1:
                if team[1] <= percentiles[0]:
                    team_color = 1
                    team_display = 10
                elif team[1] <= percentiles[1]:
                    team_color = 2
                    team_display = 25
                elif team[1] <= percentiles[2]:
                    team_color = 3
                    team_display = 50
                elif team[1] <= percentiles[3]:
                    team_color = 4
                    team_display = 75
                else:
                    team_color = 5
                    team_display = 90

                query = "UPDATE " + CEA_table + " SET " + CEA_table + ".Summary3Format = " \
                        + str(team_color) + ", " + CEA_table + ".Summary3Display = "\
                        + str(team_display) + ", " + CEA_table + ".Summary3Value = " + str(team_display) \
                        + " WHERE " + CEA_table + ".Team = '" + str(team[0]) \
                        + "' AND " + CEA_table + ".AnalysisTypeID = " + str(analysis_type) + " ;"
                #print(query);
                self._run_query(query)
                self.conn.commit()
        else:
            print('Ranking data was not found in the db')

    # run the _rankTeamsSingle for all analysis types in the analysisTypeList defined in this function
    def _rankTeamsAll(self):
        analysisTypeList=[10, 11, 20, 21, 22, 30, 60, 61, 62]
        for analysisType in analysisTypeList:
            # print(analysisType)
            self._rankTeamsSingle(analysisType)


    # Function to insert an rsCEA record into the DB.
    def _insertAnalysis(self, rsCEA):
        rsCEA_records = rsCEA.items()
        # Get the columnHeadings and values, do some formatting, and then use the _run_query function to run the
        #   query and the conn.commit to insert into the DB.
        columnHeadings = str(tuple([record[0] for record in rsCEA_records])).replace("'", "")
        values = str(tuple([record[1] for record in rsCEA_records]))

        # Insert the records into the DB
        self._run_query("INSERT INTO " + CEA_table + " "
                        + columnHeadings + " VALUES "
                        + values + ";")
        # print(columnHeadings + values)
        self.conn.commit()


# This initizlzes the analysis Class and thus runs the program.
if __name__ == '__main__':
    myAnalysis = analysis()
    
