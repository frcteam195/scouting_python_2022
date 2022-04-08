import statistics

def summManuverability(analysis, rsRobotMatches):
    # start = time.time()
    # print("teleop time:")
    # Initialize the rsCEA record set and define variables specific to this function which lie outside the for loop
    rsCEA = {}
    rsCEA['AnalysisTypeID'] = 52
    numberOfMatchesPlayed = 0
    manuverabilityList = []


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
            summManuverability = matchResults[analysis.columns.index('SummManuverability')]
            if summManuverability is None:
                summManuverability = 999
                summManuverabilityDisplay = '999'
                summManuverabilityValue = 999
                summManuverabilityFormat = 6
            elif summManuverability == 0:
                summManuverabilityDisplay = '0'
                summManuverabilityFormat = 1
                summManuverabilityValue = 0
                manuverabilityList.append(summManuverabilityValue)
            elif summManuverability == 1:
                summManuverabilityDisplay = '1'
                summManuverabilityFormat = 2
                summManuverabilityValue = 1
                manuverabilityList.append(summManuverabilityValue)
            elif summManuverability == 2:
                summManuverabilityDisplay = '2'
                summManuverabilityFormat = 3
                summManuverabilityValue = 2
                manuverabilityList.append(summManuverabilityValue)
            elif summManuverability == 1:
                summManuverabilityDisplay = '3'
                summManuverabilityFormat = 4
                summManuverabilityValue = 3
                manuverabilityList.append(summManuverabilityValue)
            elif summManuverability == 1:
                summManuverabilityDisplay = '4'
                summManuverabilityFormat = 5
                summManuverabilityValue = 4
                manuverabilityList.append(summManuverabilityValue)
            else:
                summManuverabilityDisplay = 'Err'
                summManuverabilityValue = 888
                summManuverabilityFormat = 7
            # Perform some calculations
            numberOfMatchesPlayed += 1

            # Create the rsCEA records for Display, Value, and Format
            rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Display'] = \
                    str(summManuverabilityDisplay)
            rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Value'] = summManuverabilityValue
            rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Format'] = summManuverabilityFormat

    # Create summary data
    if numberOfMatchesPlayed > 0:
        if manuverabilityList:
            rsCEA['Summary1Display'] = round(statistics.mean(manuverabilityList), 1)
            rsCEA['Summary1Value'] = round(statistics.mean(manuverabilityList), 1)
       

    # end = time.time()
    # print(end - start)

    return rsCEA
