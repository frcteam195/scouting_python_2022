import numpy as np


def playedDefense(analysis, rsRobotMatches):
    # Initialize the rsCEA record set and define variables specific to this function which lie outside the for loop
    rsCEA = {}
    rsCEA['AnalysisTypeID'] = 25
    numberOfMatchesPlayed = 0
    playedDefenseList = []

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
            playedDefense = matchResults[analysis.columns.index('SummPlayedDefense')]
            if playedDefense is None:
                playedDefense = 0
            if playedDefense == 0:
                playedDefenseString = 'No'
            else:
                playedDefenseString = 'Yes'
                numberOfMatchesPlayed += 1
                playedDefenseList.append(playedDefense)

            rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Display'] = \
                playedDefenseString
            rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Value'] = \
                playedDefense
            if playedDefense == 0:
                rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Format'] = 2
            else:
                rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Format'] = 4

    if numberOfMatchesPlayed > 0:
        # Summary1 is the % of matches where they lost Comm
        # print(playedDefenseList)
        rsCEA['Summary1Display'] = round(np.sum(playedDefenseList) / numberOfMatchesPlayed * 100)

    return rsCEA
