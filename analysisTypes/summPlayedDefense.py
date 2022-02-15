import statistics

def summPlayedDefense(analysis, rsRobotMatches):
    # start = time.time()
    # print("teleop time:")
    # Initialize the rsCEA record set and define variables specific to this function which lie outside the for loop
    rsCEA = {}
    rsCEA['AnalysisTypeID'] = 46
    numberOfMatchesPlayed = 0
    summPlayedDefenseList = []


    # Loop through each match the robot played in.
    for matchResults in rsRobotMatches:
        # This is sort of dumb as rsCEA Team and EventID will be overwritten for each match, but easier
        #   to overwite it up to 12 times than to fix at this time.
        rsCEA['Team'] = matchResults[analysis.columns.index('Team')]
        rsCEA['EventID'] = matchResults[analysis.columns.index('EventID')]
        scoutingStatus = matchResults[analysis.columns.index('ScoutingStatus')]
        if scoutingStatus == 2:
            rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Display'] = 'UR'
        else:
            # Retrieve values from the matchResults and set to appropriate variables
            summPlayedDefense = matchResults[analysis.columns.index('SummPlayedDefense')]
            if summPlayedDefense is None:
                summPlayedDefense = 999
            if summPlayedDefense == 0:
                summPlayedDefenseDisplay = 'N'
                summPlayedDefenseFormat = 2
                summPlayedDefenseValue = 0
                summPlayedDefense.append(summPlayedDefenseValue)
            if summPlayedDefense == 1:
                summPlayedDefenseDisplay = 'Y'
                summPlayedDefenseFormat = 4
                summPlayedDefenseValue = 1
                summPlayedDefenseList.append(summPlayedDefenseValue)

            # Perform some calculations
            numberOfMatchesPlayed += 1

            # Create the rsCEA records for Display, Value, and Format
            rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Display'] = \
                    str(summPlayedDefenseDisplay)
            rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Value'] = summPlayedDefenseValue
            rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Format'] = summPlayedDefenseFormat

    # Create summary data
    if numberOfMatchesPlayed > 0:
        rsCEA['Summary1Display'] = round(statistics.mean(summPlayedDefenseList), 2)
        rsCEA['Summary1Value'] = round(statistics.mean(summPlayedDefenseList), 2)
        # Some test code for calculating min, max, quantiles
        #print(min(totalBallsList))
        #print(max(totalBallsList))
        #testList = [22, 33, 44, 23, 43, 56, 43, 56, 76, 99, 23, 1, 109, 34, 76, 89, 99, 23, 55]
        #print(np.quantile(testList, 0.25))

    # end = time.time()
    # print(end - start)

    return rsCEA
