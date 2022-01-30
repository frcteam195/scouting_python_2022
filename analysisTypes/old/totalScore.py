import statistics


def totalScore(analysis, rsRobotMatches):
    # Initialize the rsCEA record set and define variables specific to this function which lie outside the for loop
    rsCEA = {}
    rsCEA['AnalysisTypeID'] = 4
    numberOfMatchesPlayed = 0
    totalPointsList = []

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
            # Identify the various different types of scoring
            if matchResults[analysis.columns.index('AutoMoveBonus')] == 1:
                autoMovePoints = 5
            else:
                autoMovePoints = 0

            autoBallsLow = matchResults[analysis.columns.index('AutoBallLow')]
            if autoBallsLow is None:
                autoBallsLow = 0

            autoBallsOuter = matchResults[analysis.columns.index('AutoBallOuter')]
            if autoBallsOuter is None:
                autoBallsOuter = 0

            autoBallsInner = matchResults[analysis.columns.index('AutoBallInner')]
            if autoBallsInner is None:
                autoBallsOuter = 0

            teleBallsLow = matchResults[analysis.columns.index('TeleBallLowZone1')]
            if teleBallsLow is None:
                teleBallsLow = 0

            TeleBallOuterZone1 = matchResults[analysis.columns.index('TeleBallOuterZone1')]
            if TeleBallOuterZone1 is None:
                TeleBallOuterZone1 = 0
            TeleBallOuterZone2 = matchResults[analysis.columns.index('TeleBallOuterZone2')]
            if TeleBallOuterZone2 is None:
                TeleBallOuterZone2 = 0
            TeleBallOuterZone3 = matchResults[analysis.columns.index('TeleBallOuterZone3')]
            if TeleBallOuterZone3 is None:
                TeleBallOuterZone3 = 0
            TeleBallOuterZone4 = matchResults[analysis.columns.index('TeleBallOuterZone4')]
            if TeleBallOuterZone4 is None:
                TeleBallOuterZone4 = 0
            TeleBallOuterZone5 = matchResults[analysis.columns.index('TeleBallOuterZone5')]
            if TeleBallOuterZone5 is None:
                TeleBallOuterZone5 = 0
            teleBallsOuter = TeleBallOuterZone1 + TeleBallOuterZone2 + TeleBallOuterZone3 + \
                             TeleBallOuterZone4 + TeleBallOuterZone5

            TeleBallInnerZone1 = matchResults[analysis.columns.index('TeleBallInnerZone1')]
            if TeleBallInnerZone1 is None:
                TeleBallInnerZone1 = 0
            TeleBallInnerZone2 = matchResults[analysis.columns.index('TeleBallInnerZone2')]
            if TeleBallInnerZone2 is None:
                TeleBallInnerZone2 = 0
            TeleBallInnerZone3 = matchResults[analysis.columns.index('TeleBallInnerZone3')]
            if TeleBallInnerZone3 is None:
                TeleBallInnerZone3 = 0
            TeleBallInnerZone4 = matchResults[analysis.columns.index('TeleBallInnerZone4')]
            if TeleBallInnerZone4 is None:
                TeleBallInnerZone4 = 0
            TeleBallInnerZone5 = matchResults[analysis.columns.index('TeleBallInnerZone5')]
            if TeleBallInnerZone5 is None:
                TeleBallInnerZone5 = 0
            teleBallsInner = TeleBallInnerZone1 + TeleBallInnerZone2 + TeleBallInnerZone3 + \
                             TeleBallInnerZone4 + TeleBallInnerZone5

            if matchResults[analysis.columns.index('TeleWheelStage2Status')] == 1:
                rotationControlPoints = 10
            else:
                rotationControlPoints = 0
            if matchResults[analysis.columns.index('TeleWheelStage3Status')] == 1:
                positionControlPoints = 20
            else:
                positionControlPoints = 0

            climbStatus = matchResults[analysis.columns.index('ClimbStatus')]
            levelStatus = matchResults[analysis.columns.index('ClimbLevelStatus')]
            if climbStatus == 2 and levelStatus == 1:
                climbPoints = 25
                parkPoints = 0
                levelPoints = 15
            elif climbStatus == 2 and levelStatus == 0:
                climbPoints = 25
                parkPoints = 0
                levelPoints = 0
            elif climbStatus == 3 or climbStatus == 5:
                climbPoints = 0
                parkPoints = 5
                levelPoints = 0
            else:
                climbPoints = 0
                parkPoints = 0
                levelPoints = 0

            # Adding up all the previously identified elements
            numberOfMatchesPlayed += 1
            totalPoints = autoMovePoints + \
                          (teleBallsLow + (autoBallsLow * 2)) + \
                          ((teleBallsOuter * 2) + (autoBallsOuter * 2 * 2)) + \
                          ((teleBallsInner * 3) + (autoBallsInner * 3 * 2)) + \
                          (rotationControlPoints + positionControlPoints) + \
                          (climbPoints + parkPoints + levelPoints)
            totalPointsList.append(totalPoints)

            # Set the Display, Value, and Format values
            rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Display'] = totalPoints
            rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Value'] = totalPoints
            if totalPoints >= 101:
                rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Format'] = 5
            elif 70 < totalPoints < 101:
                rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Format'] = 4
            elif 40 < totalPoints < 71:
                rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Format'] = 3
            elif 10 < totalPoints < 41:
                rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Format'] = 2
            else:
                rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Format'] = 1

    # Set the summary questions
    if numberOfMatchesPlayed > 0:
        rsCEA['Summary1Display'] = round(statistics.mean(totalPointsList), 1)
        rsCEA['Summary1Value'] = round(statistics.mean(totalPointsList), 1)
        rsCEA['Summary2Display'] = statistics.median(totalPointsList)
        rsCEA['Summary2Value'] = statistics.median(totalPointsList)

    return rsCEA
