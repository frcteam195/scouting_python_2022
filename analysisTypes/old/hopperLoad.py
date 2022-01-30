import numpy as np


def hopperLoad(analysis, rsRobotMatches):
    # Initialize the rsCEA record set and define variables specific to this function which lie outside the for loop
    rsCEA = {}
    rsCEA['AnalysisTypeID'] = 24
    numberOfMatchesPlayed = 0
    hopperLoad = 0
    hopperLoadString = ''
    hopperLoadList = []

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
            hopperLoad = matchResults[analysis.columns.index('SummHopperLoad')]
            if hopperLoad is None:
                hopperLoad = 0
            elif hopperLoad == 0:
                hopperLoadString = 'No'
            else:
                hopperLoadString = 'Yes'

            # Perform some calculations
            numberOfMatchesPlayed += 1
            hopperLoadList.append(hopperLoad)

            # Create the rsCEA records for Display, Value, and Format
            rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Display'] = hopperLoadString
            rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Value'] = hopperLoad
            if hopperLoad == 0:
                rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Format'] = 2
            else:
                rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Format'] = 4

    # Create summary data
    if numberOfMatchesPlayed > 0:
        # Summary1 is the % of matches where they lost Comm
        rsCEA['Summary1Display'] = round(np.sum(hopperLoadList)/numberOfMatchesPlayed * 100)

    return rsCEA