import statistics

def BACargoRP(analysis, rsRobotMatches):
    # start = time.time()
    # print("teleop time:")
    # Initialize the rsCEA record set and define variables specific to this function which lie outside the for loop
    rsCEA = {}
    rsCEA['AnalysisTypeID'] = 74
    numberOfMatchesPlayed = 0
    BACargoRPList = []


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
            BACargoRP = matchResults[analysis.columns.index('BACargoRP')]
            if BACargoRP is None:
                BACargoRPDisplay = "-"
                BACargoRPFormat = 6
                BACargoRP = 0
            elif BACargoRP == 0:
                BACargoRPFormat = 2
                BACargoRPDisplay = BACargoRP
            else:
                BACargoRPDisplay = BACargoRP
                BACargoRPFormat = 4

            BACargoRPList.append(BACargoRP)

            # Perform some calculations
            numberOfMatchesPlayed += 1

            # Create the rsCEA records for Display, Value, and Format
            rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Display'] = \
                    str(BACargoRPDisplay)
            rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Value'] = BACargoRP
            rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Format'] = BACargoRPFormat

    if numberOfMatchesPlayed > 0:
        rsCEA['Summary1Display'] = round(statistics.mean(BACargoRPList), 1)
        rsCEA['Summary1Value'] = round(statistics.mean(BACargoRPList), 1)
        rsCEA['Summary2Display'] = round(statistics.median(BACargoRPList), 1)
        rsCEA['Summary2Value'] = round(statistics.median(BACargoRPList), 1)
        rsCEA['Summary4Display'] = round(statistics.mean(BACargoRPList), 1)
        rsCEA['Summary4Value'] = round(statistics.mean(BACargoRPList), 1)

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
