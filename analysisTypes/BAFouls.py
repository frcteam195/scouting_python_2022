import statistics

def BAFouls(analysis, rsRobotMatches):
    # start = time.time()
    # print("teleop time:")
    # Initialize the rsCEA record set and define variables specific to this function which lie outside the for loop
    rsCEA = {}
    rsCEA['AnalysisTypeID'] = 73
    numberOfMatchesPlayed = 0
    BAFoulsList = []
    BATechFoulsList = []


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
            BAFouls = matchResults[analysis.columns.index('BAFouls')]
            BATechFouls = matchResults[analysis.columns.index('BATechFouls')]
            if BAFouls is None:
                BAFouls = -1
                BAFoulsDisplay = "-"
                BAFoulsFormat = 6
            else:
                BAFoulsDisplay = BAFouls

            if BATechFouls is None:
                BATechFouls = -1
                BATechFoulsDisplay = "-"
            else:
                BATechFoulsDisplay = BATechFouls

            # Perform some calculations
            numberOfMatchesPlayed += 1
            BAFoulsList.append(BAFouls)
            BATechFoulsList.append(BATechFouls)
            BAFoulsPoints = BAFouls * 4
            BATechFoulsPoints = BATechFouls * 8
            BATotalPoints = BAFoulsPoints + BATechFoulsPoints

            # Set values for formats
            if 4 > BATotalPoints >= 0:
                BAFoulsFormat = 5
            elif 8 > BATotalPoints >= 4:
                BAFoulsFormat = 4
            elif 12 > BATotalPoints >=8:
                BAFoulsFormat = 3
            elif 16 > BATotalPoints >= 12:
                BAFoulsFormat = 2
            elif BATotalPoints >= 16:
                BAFoulsFormat = 1

            # Create the rsCEA records for Display, Value, and Format
            rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Display'] = \
                    str(BAFoulsDisplay) + "|" + str(BATechFoulsDisplay)
            rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Value'] = BAFouls
            rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Format'] = BAFoulsFormat

    if numberOfMatchesPlayed > 0:
        rsCEA['Summary1Display'] = round(statistics.mean(BAFoulsList), 1)
        rsCEA['Summary1Value'] = round(statistics.mean(BAFoulsList), 1)
        rsCEA['Summary2Display'] = round(statistics.median(BAFoulsList), 1)
        rsCEA['Summary2Value'] = round(statistics.median(BAFoulsList), 1)
        rsCEA['Summary4Display'] = round(statistics.mean(BAFoulsList), 1)
        rsCEA['Summary4Value'] = round(statistics.mean(BAFoulsList), 1)

    # Create BAary data
    #if numberOfMatchesPlayed > 0:
    #    rsCEA['Summary1Display'] = round(statistics.mean(foulsList), 2)
    #    rsCEA['Summary1Value'] = round(statistics.mean(foulsList), 2)
        # Some test code for calculating min, max, quantiles
        #print(min(totalBallsList))
        #print(max(totalBallsList))
        #testList = [22, 33, 44, 23, 43, 56, 43, 56, 76, 99, 23, 1, 109, 34, 76, 89, 99, 23, 55]
        #print(np.quantile(testList, 0.25))

    # end = time.time()
    # print(end - start)

    return rsCEA
