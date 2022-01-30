import numpy as np


def groundPickup(analysis, rsRobotMatches):
    # Initialize the rsCEA record set and define variables specific to this function which lie outside the for loop
    rsCEA = {}
    rsCEA['AnalysisTypeID'] = 23
    numberOfMatchesPlayed = 0

    groundPickupList  = []

    # Loop through each match the robot played in.
    for matchResults in rsRobotMatches:
        rsCEA['Team'] = matchResults[analysis.columns.index('Team')]
        rsCEA['EventID'] = matchResults[analysis.columns.index('EventID')]
        autoDidNotShow = matchResults[analysis.columns.index('AutoDidNotShow')]
        scoutingStatus = matchResults[analysis.columns.index('ScoutingStatus')]
        # Skip if DNS or UR
        if autoDidNotShow == 1:
            rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Display'] = ''
        elif scoutingStatus == 2:
            rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Display'] = ''
        else:
            # Retrieve values from the matchResults and set to appropriate variables
            groundPickup = matchResults[analysis.columns.index('SummGroundPickup')]
            if groundPickup is None:
                groundPickup = 0
            if groundPickup == 0:
                groundPickupString = 'No'
            else:
                groundPickupString = 'Yes'

            # Perform some calculations
            numberOfMatchesPlayed += 1
            groundPickupList.append(groundPickup)

            # Create the rsCEA records for Dsiplay, Value, and Format
            rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Display'] = groundPickupString
            rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Value'] = groundPickup
            if groundPickup == 0:
                rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Format'] = 2
            else:
                rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Format'] = 4


    # Create summary data
    if numberOfMatchesPlayed > 0:
        # Summary1 is the % of matches where they performed a Ground Pickup
        rsCEA['Summary1Display'] = (round(np.sum(groundPickupList) / numberOfMatchesPlayed * 100))

    return rsCEA
