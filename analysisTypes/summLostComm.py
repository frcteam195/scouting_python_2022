import statistics

def summLostComm(analysis, rsRobotMatches):
    # start = time.time()
    # print("teleop time:")
    # Initialize the rsCEA record set and define variables specific to this function which lie outside the for loop
    rsCEA = {}
    rsCEA['AnalysisTypeID'] = 47
    numberOfMatchesPlayed = 0
    lostCommList = []


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
            summLostComm = matchResults[analysis.columns.index('SummLostComm')]
            if summLostComm is None:
                summLostComm = 999
                summLostCommDisplay = '999'
            elif summLostComm == 0:
                summLostCommDisplay = 'N'
                summLostCommFormat = 4
                summLostCommValue = 0
                lostCommList.append(summLostCommValue)
            elif summLostComm == 1:
                summLostCommDisplay = 'Y'
                summLostCommFormat = 2
                summLostCommValue = 1
                lostCommList.append(summLostCommValue)
            else:
                summLostCommDisplay = 'Err'

            # Perform some calculations
            numberOfMatchesPlayed += 1

            # Create the rsCEA records for Display, Value, and Format
            rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Display'] = \
                    str(summLostCommDisplay)
            rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Value'] = summLostCommValue
            rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Format'] = summLostCommFormat

    # Create summary data
    if numberOfMatchesPlayed > 0:
        rsCEA['Summary1Display'] = round(statistics.mean(lostCommList), 2)
        rsCEA['Summary1Value'] = round(statistics.mean(lostCommList), 2)
        # Some test code for calculating min, max, quantiles
        #print(min(totalBallsList))
        #print(max(totalBallsList))
        #testList = [22, 33, 44, 23, 43, 56, 43, 56, 76, 99, 23, 1, 109, 34, 76, 89, 99, 23, 55]
        #print(np.quantile(testList, 0.25))

    # end = time.time()
    # print(end - start)

    return rsCEA
