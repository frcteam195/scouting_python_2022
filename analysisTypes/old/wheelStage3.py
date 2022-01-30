import statistics
import numpy as np


def wheelStage3(analysis, rsRobotMatches):
    # Initialize the rsCEA record set and define variables specific to this function which lie outside the for loop
    rsCEA = {}
    rsCEA['AnalysisTypeID'] = 6
    numberOfMatchesPlayed = 0
    sucessTotal = 0
    timeList = []

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
            numberOfMatchesPlayed += 1
            wheelStage3Status = matchResults[analysis.columns.index('TeleWheelStage3Status')]
            wheelStage3Time = matchResults[analysis.columns.index('TeleWheelStage3Time')]
            wheelStage3Attempts = matchResults[analysis.columns.index('TeleWheelStage3Attempts')]
            if wheelStage3Attempts > 1:
                wheelStage3AttemptsString = '*'
            else:
                wheelStage3AttemptsString = ''

            if wheelStage3Status == 0 and wheelStage3Attempts == 0:  # No attempt:
                rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Display'] = '-'
                rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Format'] = 0
                timeList.append(0)
            elif wheelStage3Status == 1:
                sucessTotal += 1
                timeList.append(wheelStage3Time)
                rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Display'] = \
                    str(wheelStage3Time) + str(wheelStage3AttemptsString)
                rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Value'] = wheelStage3Time
                if wheelStage3Time <= 5:
                    rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Format'] = 5
                elif 5 < wheelStage3Time <= 10:
                    rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Format'] = 4
                elif 10 < wheelStage3Time <= 15:
                    rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Format'] = 3
                else:
                    rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Format'] = 2
            else:
                rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Display'] = \
                    str(wheelStage3Time) + str(wheelStage3AttemptsString)
                rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Format'] = 1

    if len(timeList) > 0:
        rsCEA['Summary1Display'] = round(statistics.mean(timeList), 1)
        rsCEA['Summary1Value'] = round(statistics.mean(timeList), 1)
        rsCEA['Summary2Display'] = str(statistics.median(timeList))
        rsCEA['Summary2Value'] = statistics.median(timeList)
        rsCEA['Summary4Display'] = str(round(sucessTotal / numberOfMatchesPlayed, 1))
        rsCEA['Summary4Value'] = round(sucessTotal / numberOfMatchesPlayed, 1)

    return rsCEA