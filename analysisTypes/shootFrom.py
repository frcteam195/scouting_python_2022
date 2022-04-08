import statistics

def shootFrom(analysis, rsRobotMatches):
    # start = time.time()
    # print("teleop time:")
    # Initialize the rsCEA record set and define variables specific to this function which lie outside the for loop
    rsCEA = {}
    rsCEA['AnalysisTypeID'] = 53
    numberOfMatchesPlayed = 0


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
            shootFrom = matchResults[analysis.columns.index('SummShootHub')]
            if shootFrom is None:
                shootFrom = 999
                shootFromDisplay = '999'
                shootFromValue = 999
                shootFromFormat = 6
            elif shootFrom == 0:
                shootFromDisplay = 'NA'
                shootFromFormat = 1
                shootFromValue = 0
            elif shootFrom == 1:
                shootFromDisplay = 'hub'
                shootFromFormat = 2
                shootFromValue = 1
            elif shootFrom == 2:
                shootFromDisplay = 'rad'
                shootFromFormat = 3
                shootFromValue = 2
            elif shootFrom == 3:
                shootFromDisplay = 'aim'
                shootFromFormat = 4
                shootFromValue = 3
            elif shootFrom == 4:
                shootFromDisplay = 'any'
                shootFromFormat = 5
                shootFromValue = 4
            else:
                shootFromDisplay = 'Err'
                shootFromValue = 888
                shootFromFormat = 7
            # Perform some calculations
            numberOfMatchesPlayed += 1

            # Create the rsCEA records for Display, Value, and Format
            rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Display'] = \
                    str(shootFromDisplay)
            rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Value'] = shootFromValue
            rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Format'] = shootFromFormat

    return rsCEA
