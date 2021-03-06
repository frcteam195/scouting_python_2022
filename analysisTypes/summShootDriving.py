import statistics

def summShootDriving(analysis, rsRobotMatches):
    # start = time.time()
    # print("teleop time:")
    # Initialize the rsCEA record set and define variables specific to this function which lie outside the for loop
    rsCEA = {}
    rsCEA['AnalysisTypeID'] = 44
    numberOfMatchesPlayed = 0
    summShootDrivingList = []


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
            summShootDriving = matchResults[analysis.columns.index('SummShootDriving')]
            if summShootDriving is None:
                summShootDriving = 999
                summShootDrivingDisplay = '999'
                summShootDrivingValue = 999
                summShootDrivingFormat = 6
            elif summShootDriving == 0:
                summShootDrivingDisplay = 'N'
                summShootDrivingFormat = 6
                summShootDrivingValue = 0
                summShootDrivingList.append(summShootDrivingValue)
            elif summShootDriving == 1:
                summShootDrivingDisplay = 'Y'
                summShootDrivingFormat = 4
                summShootDrivingValue = 1
                summShootDrivingList.append(summShootDrivingValue)
            else:
                summShootDrivingDisplay = 'Err'
                summShootDrivingValue = 888
                summShootDrivingFormat = 7

            # Perform some calculations
            numberOfMatchesPlayed += 1

            # Create the rsCEA records for Display, Value, and Format
            rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Display'] = \
                    str(summShootDrivingDisplay)
            rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Value'] = summShootDrivingValue
            rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Format'] = summShootDrivingFormat

    # Create summary data
    if numberOfMatchesPlayed > 0:
        rsCEA['Summary1Display'] = round(statistics.mean(summShootDrivingList), 2)
        rsCEA['Summary1Value'] = round(statistics.mean(summShootDrivingList), 2)
        # Some test code for calculating min, max, quantiles
        #print(min(totalBallsList))
        #print(max(totalBallsList))
        #testList = [22, 33, 44, 23, 43, 56, 43, 56, 76, 99, 23, 1, 109, 34, 76, 89, 99, 23, 55]
        #print(np.quantile(testList, 0.25))

    # end = time.time()
    # print(end - start)

    return rsCEA
