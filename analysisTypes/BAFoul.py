import statistics

def BAFouls(analysis, rsRobotMatches):
    # start = time.time()
    # print("teleop time:")
    # Initialize the rsCEA record set and define variables specific to this function which lie outside the for loop
    rsCEA = {}
    rsCEA['AnalysisTypeID'] = 73
    numberOfMatchesPlayed = 0
    foulsList = []


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
            if BAFouls is None:
                BAFouls = 999
                BAFoulsDisplay = '-'
                BAFoulsValue = 999
                BAFoulsFormat = 6
            elif BAFouls >= 0:
                BAFoulsDisplay = 'BAFouls'
                BAFoulsFormat = 1
                BAFoulsValue = 0
                foulsList.append(BAFoulsValue)
            elif BAFouls >= 1:
                BAFoulsDisplay = 'BAFouls'
                BAFoulsFormat = 2
                BAFoulsValue = 1
                foulsList.append(BAFoulsValue)
            elif BAFouls >= 5:
                BAFoulsDisplay = 'BAFouls'
                BAFoulsFormat = 3
                BAFoulsValue = 2
                foulsList.append(BAFoulsValue)
            elif BAFouls >= 9:
                BAFoulsDisplay = 'BAFouls'
                BAFoulsFormat = 4
                BAFoulsValue = 3
                foulsList.append(BAFoulsValue)
            elif BAFouls >= 13:
                BAFoulsDisplay = 'BAFouls'
                BAFoulsFormat = 5
                BAFoulsValue = 4
                foulsList.append(BAFoulsValue)
            else:
                BAFoulsDisplay = 'Err'
                BAFoulsValue = 888
                BAFoulsFormat = 7

            # Perform some calculations
            numberOfMatchesPlayed += 1

            # Create the rsCEA records for Display, Value, and Format
            rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Display'] = \
                    str(BAFoulsDisplay)
            rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Value'] = BAFoulsValue
            rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Format'] = BAFoulsFormat

    # Create BAary data
    if numberOfMatchesPlayed > 0:
        rsCEA['Summary1Display'] = round(statistics.mean(foulsList), 2)
        rsCEA['Summary1Value'] = round(statistics.mean(foulsList), 2)
        # Some test code for calculating min, max, quantiles
        #print(min(totalBallsList))
        #print(max(totalBallsList))
        #testList = [22, 33, 44, 23, 43, 56, 43, 56, 76, 99, 23, 1, 109, 34, 76, 89, 99, 23, 55]
        #print(np.quantile(testList, 0.25))

    # end = time.time()
    # print(end - start)

    return rsCEA
