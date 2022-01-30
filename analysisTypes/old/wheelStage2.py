import statistics


def wheelStage2(analysis, rsRobotMatches):
    # Initialize the rsCEA record set and define variables specific to this function which lie outside the for loop
    rsCEA = {}
    rsCEA['AnalysisTypeID'] = 5
    numberOfMatchesPlayed = 0
    sucessTotal = 0
    timeList = []

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
            wheelStage2Status = matchResults[analysis.columns.index('TeleWheelStage2Status')]
            wheelStage2Time = matchResults[analysis.columns.index('TeleWheelStage2Time')]
            wheelStage2Attempts = matchResults[analysis.columns.index('TeleWheelStage2Attempts')]
            if wheelStage2Attempts > 1:
                wheelStage2AttemptsString = '*'
            else:
                wheelStage2AttemptsString = ''

            if wheelStage2Status == 0 and wheelStage2Attempts == 0:  # No attempt
                rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Display'] = '-'
                rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Format'] = 0
                timeList.append(0)
            elif wheelStage2Status == 1:  # success at the wheel
                sucessTotal += 1
                timeList.append(wheelStage2Time)  # only putting times in the list when there is a success
                rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Display'] = \
                    str(wheelStage2Time) + str(wheelStage2AttemptsString)
                rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Value'] = wheelStage2Time
                if wheelStage2Time <= 5:
                    rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Format'] = 5
                elif 5 < wheelStage2Time <= 10:
                    rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Format'] = 4
                elif 10 < wheelStage2Time <= 15:
                    rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Format'] = 3
                else:
                    rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Format'] = 2
            else:  # attempt, but failure
                rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Display'] = \
                    str(wheelStage2Time) + str(wheelStage2AttemptsString)
                rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Format'] = 1

    if len(timeList) > 0:
        rsCEA['Summary1Display'] = round(statistics.mean(timeList), 1)
        rsCEA['Summary1Value'] = round(statistics.mean(timeList), 1)
        rsCEA['Summary2Display'] = str(statistics.median(timeList))
        rsCEA['Summary2Value'] =  statistics.median(timeList)
        rsCEA['Summary4Display'] = str(round(sucessTotal / numberOfMatchesPlayed, 1))
        rsCEA['Summary4Value'] = round(sucessTotal / numberOfMatchesPlayed, 1)

    return rsCEA
