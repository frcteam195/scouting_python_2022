import statistics

def teleTotalBalls(analysis, rsRobotMatches):
    # start = time.time()
    # print("teleop time:")
    # Initialize the rsCEA record set and define variables specific to this function which lie outside the for loop
    rsCEA = {}
    rsCEA['AnalysisTypeID'] = 22
    numberOfMatchesPlayed = 0

    totalHighBallsList = []
    totalBallsList = []

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
            teleBallLow = matchResults[analysis.columns.index('TeleBallLow')]
            if teleBallLow is None:
                teleBallLow = 0
            
            teleBallHigh = matchResults[analysis.columns.index('TeleBallHigh')]
            if teleBallHigh is None:
                teleBallHigh = 0
            
            teleBallMiss = matchResults[analysis.columns.index('TeleBallMiss')]
            if teleBallMiss is None:
                teleBallMiss = 0
            
            defPlayedAgainst = matchResults[analysis.columns.index('SummDefPlayedAgainst')]
            if defPlayedAgainst is None:
                defPlayedAgainst = 0

            # Perform some calculations
            numberOfMatchesPlayed += 1
            totalBalls = teleBallLow + teleBallHigh
            totalHighBallsList.append(teleBallHigh)
            totalBallsList.append(teleBallLow + teleBallHigh)

            # Create the rsCEA records for Display, Value, and Format
            if defPlayedAgainst == 0:
                rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Display'] = \
                    str(totalBalls) + "|" + str(teleBallHigh)
            else:
                rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Display'] = \
                    str(totalBalls) + "|" + str(teleBallHigh) + "*"
            rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Value'] = totalBalls
            if totalBalls >= 16:
                rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Format'] = 5
            elif totalBalls >= 10:
                rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Format'] = 4
            elif totalBalls >= 5:
                rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Format'] = 3
            elif totalBalls >= 1:
                rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Format'] = 2
            else:
                rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Format'] = 1

    # Create summary data
    if numberOfMatchesPlayed > 0:
        rsCEA['Summary1Display'] = round(statistics.mean(totalBallsList), 1)
        rsCEA['Summary1Value'] = round(statistics.mean(totalBallsList), 1)
        rsCEA['Summary2Display'] = round(statistics.median(totalBallsList), 1)
        rsCEA['Summary2Value'] = round(statistics.median(totalBallsList), 1)
        rsCEA['Summary4Display'] = round(statistics.mean(totalHighBallsList), 1)
        rsCEA['Summary4Value'] = round(statistics.mean(totalHighBallsList), 1)

        # Some test code for calculating min, max, quantiles
        #print(min(totalBallsList))
        #print(max(totalBallsList))
        #testList = [22, 33, 44, 23, 43, 56, 43, 56, 76, 99, 23, 1, 109, 34, 76, 89, 99, 23, 55]
        #print(np.quantile(testList, 0.25))

    # end = time.time()
    # print(end - start)

    return rsCEA
