import statistics

def summSpeed(analysis, rsRobotMatches):
    # start = time.time()
    # print("teleop time:")
    # Initialize the rsCEA record set and define variables specific to this function which lie outside the for loop
    rsCEA = {}
    rsCEA['AnalysisTypeID'] = 51
    numberOfMatchesPlayed = 0
    speedList = []


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
            summSpeed = matchResults[analysis.columns.index('SummSpeed')]
            if summSpeed is None:
                summSpeed = 999
                summSpeedDisplay = '999'
                summSpeedValue = 999
                summSpeedFormat = 6
            elif summSpeed == 0:
                summSpeedDisplay = '0'
                summSpeedFormat = 1
                summSpeedValue = 0
                speedList.append(summSpeedValue)
            elif summSpeed == 1:
                summSpeedDisplay = '1'
                summSpeedFormat = 2
                summSpeedValue = 1
                speedList.append(summSpeedValue)
            elif summSpeed == 2:
                summSpeedDisplay = '2'
                summSpeedFormat = 3
                summSpeedValue = 2
                speedList.append(summSpeedValue)
            elif summSpeed == 3:
                summSpeedDisplay = '3'
                summSpeedFormat = 4
                summSpeedValue = 3
                speedList.append(summSpeedValue)
            elif summSpeed == 4:
                summSpeedDisplay = '4'
                summSpeedFormat = 5
                summSpeedValue = 4
                speedList.append(summSpeedValue)
            else:
                summSpeedDisplay = 'Err'
                summSpeedValue = 888
                summSpeedFormat = 7
            # Perform some calculations
            numberOfMatchesPlayed += 1

            # Create the rsCEA records for Display, Value, and Format
            rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Display'] = \
                    str(summSpeedDisplay)
            rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Value'] = summSpeedValue
            rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Format'] = summSpeedFormat

    # Create summary data
    if numberOfMatchesPlayed > 0:
        rsCEA['Summary1Display'] = round(statistics.mean(speedList), 1)
        rsCEA['Summary1Value'] = round(statistics.mean(speedList), 1)
        # Some test code for calculating min, max, quantiles
        #print(min(totalBallsList))
        #print(max(totalBallsList))
        #testList = [22, 33, 44, 23, 43, 56, 43, 56, 76, 99, 23, 1, 109, 34, 76, 89, 99, 23, 55]
        #print(np.quantile(testList, 0.25))

    # end = time.time()
    # print(end - start)

    return rsCEA
