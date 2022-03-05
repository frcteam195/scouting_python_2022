import statistics

def summSubSystemBroke(analysis, rsRobotMatches):
    # start = time.time()
    # print("teleop time:")
    # Initialize the rsCEA record set and define variables specific to this function which lie outside the for loop
    rsCEA = {}
    rsCEA['AnalysisTypeID'] = 48
    numberOfMatchesPlayed = 0
    summSubSystemBrokeList = []


    # Loop through each match the robot played in.
    for matchResults in rsRobotMatches:
        # This is sort of dumb as rsCEA Team and EventID will be overwritten for each match, but easier
        #   to overwite it up to 12 times than to fix at this time.
        rsCEA['Team'] = matchResults[analysis.columns.index('Team')]
        rsCEA['EventID'] = matchResults[analysis.columns.index('EventID')]
        autoDidNotShow = matchResults[analysis.columns.index('AutoDidNotShow')]
        scoutingStatus = matchResults[analysis.columns.index('ScoutingStatus')]
        if autoDidNotShow == 1:
            rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Display'] = 'DNS'
        elif scoutingStatus == 2:
            rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Display'] = 'UR'
        else:
            # Retrieve values from the matchResults and set to appropriate variables
            summSubSystemBroke = matchResults[analysis.columns.index('SummSubSystemBroke')]
            if summSubSystemBroke is None:
                summSubSystemBroke = 999
                summSubSystemBrokeDisplay = '999'
                summSubSystemBrokeValue = 999
                summSubSystemBrokeFormat = 0
            elif summSubSystemBroke == 0:
                summSubSystemBrokeDisplay = 'N'
                summSubSystemBrokeFormat = 4
                summSubSystemBrokeValue = 0
                summSubSystemBrokeList.append(summSubSystemBrokeValue)
            elif summSubSystemBroke == 1:
                summSubSystemBrokeDisplay = 'Y'
                summSubSystemBrokeFormat = 2
                summSubSystemBrokeValue = 1
                summSubSystemBrokeList.append(summSubSystemBrokeValue)
            else:
                summSubSystemBrokeDisplay = 'Err'
                summSubSystemBrokeValue = 999
                summSubSystemBrokeFormat = 0

            # Perform some calculations
            numberOfMatchesPlayed += 1

            # Create the rsCEA records for Display, Value, and Format
            rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Display'] = \
                    str(summSubSystemBrokeDisplay)
            rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Value'] = summSubSystemBrokeValue
            rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Format'] = summSubSystemBrokeFormat

    # Create summary data
    if numberOfMatchesPlayed > 0:
        rsCEA['Summary1Display'] = round(statistics.mean(summSubSystemBrokeList), 2)
        rsCEA['Summary1Value'] = round(statistics.mean(summSubSystemBrokeList), 2)
        # Some test code for calculating min, max, quantiles
        #print(min(totalBallsList))
        #print(max(totalBallsList))
        #testList = [22, 33, 44, 23, 43, 56, 43, 56, 76, 99, 23, 1, 109, 34, 76, 89, 99, 23, 55]
        #print(np.quantile(testList, 0.25))

    # end = time.time()
    # print(end - start)

    return rsCEA
