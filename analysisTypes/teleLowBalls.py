import statistics


def teleLowBalls(analysis, rsRobotMatches):
    # Initialize the rsCEA record set and define variables specific to this function which lie outside the for loop
    rsCEA = {}
    rsCEA['AnalysisTypeID'] = 20
    numberOfMatchesPlayed = 0
    totalLowBallsList = []
    totalBallsList = []

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
            teleBallLow = matchResults[analysis.columns.index('TeleBallLow')]
            if teleBallLow is None:
                teleBallLow = 0
            
            teleBallHigh = matchResults[analysis.columns.index('TeleBallHigh')]
            if teleBallHigh is None:
                teleBallHigh = 0
            
            teleBallMiss = matchResults[analysis.columns.index('TeleBallMiss')]
            if teleBallMiss is None:
                teleBallMiss = 0
            
            defPlayedAgainst = matchResults[analysis.columns.index('SummDefPlayedAgainst')]
            if defPlayedAgainst is None:
                defPlayedAgainst = 0

            # Perform some calculations
            numberOfMatchesPlayed += 1
            totalTeleBalls = teleBallLow + teleBallHigh
            totalLowBallsList.append(teleBallLow)
            totalBallsList.append(totalTeleBalls)

            if defPlayedAgainst == 0:
                rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Display'] = \
                    str(teleBallLow) + "|" + str(totalTeleBalls)
            else:
                rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Display'] = \
                    str(teleBallLow) + "|" + str(totalTeleBalls) + "*"
            rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Value'] = teleBallLow
            if teleBallLow >= 16:
                rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Format'] = 5
            elif teleBallLow >= 10:
                rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Format'] = 4
            elif teleBallLow >= 5:
                rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Format'] = 3
            elif teleBallLow >= 1:
                rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Format'] = 2
            else:
                rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Format'] = 1

    if numberOfMatchesPlayed > 0:
        rsCEA['Summary1Display'] = round(statistics.mean(totalLowBallsList), 1)
        rsCEA['Summary1Value'] = round(statistics.mean(totalLowBallsList), 1)
        rsCEA['Summary2Display'] = statistics.median(totalLowBallsList)
        rsCEA['Summary2Value'] = statistics.median(totalLowBallsList)
        # summary 3 will be used for rank
        rsCEA['Summary4Display'] = round(statistics.mean(totalBallsList), 1)
        rsCEA['Summary4Value'] = round(statistics.mean(totalBallsList), 1)

    return rsCEA
