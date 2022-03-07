import statistics
import numpy as np


# ******************** AnalysisTypeID = 9 = lostComm *******************

def summBrokeDown(analysis, rsRobotMatches):
    # Initialize the rsCEA record set and define variables specific to this function which lie outside the for loop
    rsCEA = {}
    rsCEA['AnalysisTypeID'] = 49
    numberOfMatchesPlayed = 0

    brokeDownList = []

    # Loop through each match the robot played in.
    for matchResults in rsRobotMatches:
        rsCEA['Team'] = matchResults[analysis.columns.index('Team')]
        rsCEA['EventID'] = matchResults[analysis.columns.index('EventID')]
        autoDidNotShow = matchResults[analysis.columns.index('AutoDidNotShow')]
        scoutingStatus = matchResults[analysis.columns.index('ScoutingStatus')]
        # Skip if DNS or UR
        if autoDidNotShow == 1:
            rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Display'] = 'DNS'
        elif scoutingStatus == 2:
            rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Display'] = 'UR'
        else:
            # Retrieve values from the matchResults and set to appropriate variables
            brokeDown = matchResults[analysis.columns.index('SummBrokeDown')]
            if brokeDown is None:
                brokeDownValue = 999
                brokeDownString = '999'
                brokeDownFormat = 6
            elif brokeDown == 0:
                brokeDownString = 'N'
                brokeDownFormat = 4
                brokeDownValue = 0
                brokeDownList.append(brokeDownValue)
            elif brokeDown == 1:
                brokeDownString = 'Y'
                brokeDownFormat = 2
                brokeDownValue = 1
                brokeDownList.append(brokeDownValue)
            else:
                brokeDownString = 'Err'
                brokeDownValue = 888
                brokeDownFormat = 7

            # Perform some calculations
            numberOfMatchesPlayed += 1
            brokeDownList.append(brokeDown)

            # Create the rsCEA records for Dsiplay, Value, and Format
            rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Display'] = brokeDownString
            rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Value'] = brokeDownValue
            rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Format'] = brokeDownFormat

    # Create summary data
    if numberOfMatchesPlayed > 0:
        # Summary1 is the % of matches where they lost Comm
        rsCEA['Summary1Display'] = round(statistics.mean(brokeDownList), 2)
        rsCEA['Summary1Value'] = round(statistics.mean(brokeDownList), 2)

    return rsCEA
