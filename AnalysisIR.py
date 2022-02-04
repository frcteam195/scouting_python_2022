import mysql.connector as mariaDB
import numpy as np
import datetime
import time
# For each analysisType we create add a new import statement. We could import all analysisTypes
# Mark is the Shark
from analysisTypes.autonomous import autonomous
# from analysisTypes.ballSummary import ballSummary
# from analysisTypes.brokeDown import brokeDown
from analysisTypes.climb import climb
# from analysisTypes.groundPickup import groundPickup
# from analysisTypes.hopperLoad import hopperLoad
# from analysisTypes.lostComm import lostComm
# from analysisTypes.matchVideos import matchVideos
# from analysisTypes.playedDefense import playedDefense
# from analysisTypes.subSBroke import subSBroke
from analysisTypes.teleTotalBalls import teleTotalBalls
# from analysisTypes.totalBalls import totalBalls
# from analysisTypes.totalInnerBalls import totalInnerBalls
# from analysisTypes.totalLowBalls import totalLowBalls
# from analysisTypes.totalOuterBalls import totalOuterBalls
# from analysisTypes.totalScore import totalScore
# from analysisTypes.totalUpperBalls import totalUpperBalls
# from analysisTypes.wheelStage2 import wheelStage2
# from analysisTypes.wheelStage3 import wheelStage3
# from analysisTypes.startingPosition import startingPosition
# from analysisTypes.ranking import ranking

CEA_table = "CurrentEventAnalysis"

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
        self.conn = mariaDB.connect(user='admin',
                                    passwd='Einstein195',
                                    host='frcteam195testinstance.cmdlvflptajw.us-east-1.rds.amazonaws.com',
                                    database='team195_scouting')
        self.cursor = self.conn.cursor()

        # Pi DB with remote access (e.g. from laptop)
        # self.conn = mariaDB.connect(user='admin',
        #                             passwd='team195',
        #                             host='10.0.0.195',
        #                             database='team195_scouting')
        # self.cursor = self.conn.cursor()

        # Pi DB with local access (e.g. from the Pi itself)
        # self.conn = mariaDB.connect(user='admin',
        #                             passwd='team195',
        #                             host='localhost',
        #                             database='team195_scouting')
        # self.cursor = self.conn.cursor()

        # Connection to AWS database with proper data
        # self.conn = mariaDB.connect(user='admin',
#                                     passwd='Einstein195',
#                                     host='frcteam195.cmdlvflptajw.us-east-1.rds.amazonaws.com',
#                                     database='team195_scouting')
#         self.cursor = self.conn.cursor()

        self.columns = []
        self._wipeCEA()
        self.rsRobots = self._getTeams()
        self._analyzeTeams()
        self._rankTeamsAll()

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
        self._run_query("DELETE FROM " + CEA_table + "")
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
            # print(rsRobotMatches)

            if rsRobotMatches:
                rsCEA = autonomous(analysis=self, rsRobotMatches=rsRobotMatches)
                self._insertAnalysis(rsCEA)

                rsCEA = teleTotalBalls(analysis=self, rsRobotMatches=rsRobotMatches)
                self._insertAnalysis(rsCEA)
                
                rsCEA = climb(analysis=self, rsRobotMatches=rsRobotMatches)
                self._insertAnalysis(rsCEA)


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
            print('Data was not found in the db')

    # run the _rankTeamsSingle for all analysis types in the analysisTypeList defined in this function
    def _rankTeamsAll(self):
        #analysisTypeList=[2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        analysisTypeList=[2]
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