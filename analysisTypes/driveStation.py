

def driveStation(analysis, rsRobotMatches):
    # Initialize the rsCEA record set and define variables specific to this function which lie outside the for loop
    rsCEA = {}
    rsCEA['AnalysisTypeID'] = 3
    numberOfMatchesPlayed = 0

    # Loop through each match the robot played in.
    for matchResults in rsRobotMatches:
        # This is sort of dumb as rsCEA Team and EventID will be overwritten for each match, but easier
        #   to overwite it up to 12 times than to fix at this time.
        rsCEA['Team'] = matchResults[analysis.columns.index('Team')]
        rsCEA['EventID'] = matchResults[analysis.columns.index('EventID')]
        # We are hijacking the starting position to write DNS or UR. This should go to Auto as it will not
        #   likely be displayed on team picker pages.
        autoDidNotShow = matchResults[analysis.columns.index('AutoDidNotShow')]
        scoutingStatus = matchResults[analysis.columns.index('ScoutingStatus')]
        if autoDidNotShow == 1:
            rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Display'] = 'DNS'
        elif scoutingStatus == 2:
            rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Display'] = 'UR'
        else:
            # Increment the number of matches played and write Match#Display, Match#Value and Match#Format
            numberOfMatchesPlayed += 1
            driveStation = matchResults[analysis.columns.index('AllianceStationID')]
            if driveStation == 1:
                driveStationDisplay = 'R1'
            elif driveStation == 2:
                driveStationDisplay = 'R2'
            elif driveStation == 3:
                driveStationDisplay = 'R3'
            elif driveStation == 4:
                driveStationDisplay = 'B1'
            elif driveStation == 5:
                driveStationDisplay = 'B2'
            elif driveStation == 6:
                driveStationDisplay = 'B3'
                
            rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Display'] = str(driveStationDisplay)
            rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Format'] = 0
            # An if statement will go here to define Match#Format

    return rsCEA