import statistics

from analysisTypes.teleTotalBalls import teleTotalBalls


def totalScore(analysis, rsRobotMatches):
    # Initialize the rsCEA record set and define variables specific to this function which lie outside the for loop
    rsCEA = {}
    rsCEA['AnalysisTypeID'] = 4
    numberOfMatchesPlayed = 0
    totalPointsList = []
    climbPoints = 0

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
            # Auto move, low ball, and high ball
            autoMoveStatus = matchResults[analysis.columns.index("AutoMoveBonus")]
            if autoMoveStatus == 2:
                autoMovePoints = 2
            else:
                autoMovePoints = 0
            
            autoBallLow = matchResults[analysis.columns.index('AutoBallLow')]
            if autoBallLow is None:
                autoBallLow = 0
            autoBallHigh = matchResults[analysis.columns.index('AutoBallHigh')]
            if autoBallHigh is None:
                autoBallHigh = 0
            
            # Tele Low ball, high ball, and climb
            teleBallLow = matchResults[analysis.columns.index('TeleBallLow')]
            if teleBallLow is None:
                teleBallLow = 0
            teleBallHigh = matchResults[analysis.columns.index('TeleBallHigh')]
            if teleBallHigh is None:
                teleBallHigh = 0
            teleBallMiss = matchResults[analysis.columns.index('TeleBallMiss')]
            
            climbStatus = matchResults[analysis.columns.index('ClimbStatusID')]
            if climbStatus != 5:
                climbPoints = 0
            if climbStatus == 5:
                climbHeight = matchResults[analysis.columns.index('ClimbHeight')]
                if climbHeight == 1:
                    climbPoints = 4    
                elif climbHeight == 2:
                    climbPoints = 6   
                elif climbHeight == 3:
                    climbPoints = 10
                elif climbHeight == 4:
                    climbPoints = 15
                else:
                    climbPoints = 999
             

            # Adding up all the previously identified elements
            numberOfMatchesPlayed += 1
            totalPoints = autoMovePoints + (autoBallHigh * 4) + (autoBallLow * 2) + \
                        (teleBallHigh * 2) + teleBallLow + climbPoints
            totalPointsList.append(totalPoints)

            # Set the Display, Value, and Format values
            rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Display'] = str(totalPoints)
            rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Value'] = totalPoints
            if totalPoints >= 61:
                rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Format'] = 5
            elif totalPoints >= 41:
                rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Format'] = 4
            elif totalPoints >= 21:
                rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Format'] = 3
            elif totalPoints >= 11:
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
