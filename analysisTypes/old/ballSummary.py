import statistics

def ballSummary(analysis, rsRobotMatches):
    # Initialize the rsCEA record set and define variables specific to this function which lie outside the for loop
    rsCEA = {}
    rsCEA['AnalysisTypeID'] = 30

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
            AutoBallsLow = matchResults[analysis.columns.index('AutoBallLow')]
            if AutoBallsLow is None:
                AutoBallsLow = 0

            AutoBallsOuter = matchResults[analysis.columns.index('AutoBallOuter')]
            if AutoBallsOuter is None:
                AutoBallsOuter = 0

            AutoBallsInner = matchResults[analysis.columns.index('AutoBallInner')]
            if AutoBallsInner is None:
                AutoBallsInner = 0

            TeleBallLowZone1 = matchResults[analysis.columns.index('TeleBallLowZone1')]
            if TeleBallLowZone1 is None:
                TeleBallLowZone1 = 0

            TeleBallOuterZone1 = matchResults[analysis.columns.index('TeleBallOuterZone1')]
            if TeleBallOuterZone1 is None:
                TeleBallOuterZone1 = 0

            TeleBallInnerZone1 = matchResults[analysis.columns.index('TeleBallInnerZone1')]
            if TeleBallInnerZone1 is None:
                TeleBallInnerZone1 = 0

            TeleBallOuterZone2 = matchResults[analysis.columns.index('TeleBallOuterZone2')]
            if TeleBallOuterZone2 is None:
                TeleBallOuterZone2 = 0

            TeleBallInnerZone2 = matchResults[analysis.columns.index('TeleBallInnerZone2')]
            if TeleBallInnerZone2 is None:
                TeleBallInnerZone2 = 0

            TeleBallOuterZone3 = matchResults[analysis.columns.index('TeleBallOuterZone3')]
            if TeleBallOuterZone3 is None:
                TeleBallOuterZone3 = 0

            TeleBallInnerZone3 = matchResults[analysis.columns.index('TeleBallInnerZone3')]
            if TeleBallInnerZone3 is None:
                TeleBallInnerZone3 = 0

            TeleBallOuterZone4 = matchResults[analysis.columns.index('TeleBallOuterZone4')]
            if TeleBallOuterZone4 is None:
                TeleBallOuterZone4 = 0

            TeleBallInnerZone4 = matchResults[analysis.columns.index('TeleBallInnerZone4')]
            if TeleBallInnerZone4 is None:
                TeleBallInnerZone4 = 0

            TeleBallOuterZone5 = matchResults[analysis.columns.index('TeleBallOuterZone5')]
            if TeleBallOuterZone5 is None:
                TeleBallOuterZone5 = 0

            TeleBallInnerZone5 = matchResults[analysis.columns.index('TeleBallInnerZone5')]
            if TeleBallInnerZone5 is None:
                TeleBallInnerZone5 = 0

            NumClimbPos1 = 0
            if matchResults[analysis.columns.index('ClimbPosition')] == 1:
                NumClimbPos1 += 1

            NumClimbPos2 = 0
            if matchResults[analysis.columns.index('ClimbPosition')] == 2:
                NumClimbPos2 += 1

            NumClimbPos3 = 0
            if matchResults[analysis.columns.index('ClimbPosition')] == 3:
                NumClimbPos3 += 1

            NumClimbPos4 = 0
            if matchResults[analysis.columns.index('ClimbPosition')] == 4:
                NumClimbPos4 += 1

            NumClimbPos5 = 0
            if matchResults[analysis.columns.index('ClimbPosition')] == 5:
                NumClimbPos5 += 1

            # Perform some calculations
            totalBallsZone1 = (TeleBallLowZone1 + TeleBallOuterZone1 + TeleBallInnerZone1)
            totalBallsZone2 = (TeleBallOuterZone2 + TeleBallInnerZone2)
            totalBallsZone3 = (TeleBallOuterZone3 + TeleBallInnerZone3)
            totalBallsZone4 = (TeleBallOuterZone4 + TeleBallInnerZone4)
            totalBallsZone5 = (TeleBallOuterZone5 + TeleBallInnerZone5)
            
            totalBallsLow = AutoBallsLow + TeleBallLowZone1
            
            totalBallsOuter = (TeleBallOuterZone1 + TeleBallOuterZone2 + TeleBallOuterZone3 + TeleBallOuterZone4 +
                               TeleBallOuterZone5 + AutoBallsOuter)
            
            totalBallsInner = (TeleBallInnerZone1 + TeleBallInnerZone2 + TeleBallInnerZone3 + TeleBallInnerZone4 +
                               TeleBallInnerZone5 + AutoBallsInner)
            
            totalBallsHigh = (totalBallsOuter + totalBallsInner)
            totalBalls = totalBallsHigh + totalBallsLow

            # Set Table Rows (Hijacked Format From Other CEA Rows)
            rsCEA['Match1Display'] = totalBallsZone1
            rsCEA['Match1Value'] = totalBallsZone1

            rsCEA['Match2Display'] = totalBallsZone2
            rsCEA['Match2Value'] = totalBallsZone2

            rsCEA['Match3Display'] = totalBallsZone3
            rsCEA['Match3Value'] = totalBallsZone3

            rsCEA['Match4Display'] = totalBallsZone4
            rsCEA['Match4Value'] = totalBallsZone4

            rsCEA['Match5Display'] = totalBallsZone5
            rsCEA['Match5Value'] = totalBallsZone5

            rsCEA['Match6Display'] = totalBallsOuter
            rsCEA['Match6Value'] = totalBallsOuter

            rsCEA['Match7Display'] = totalBallsInner
            rsCEA['Match7Value'] = totalBallsInner

            rsCEA['Match8Display'] = totalBallsHigh
            rsCEA['Match8Value'] = totalBallsHigh

            rsCEA['Match9Display'] = totalBallsLow
            rsCEA['Match9Value'] = totalBallsLow

            rsCEA['Match10Display'] = totalBalls
            rsCEA['Match10Value'] = totalBalls

            rsCEA['Match11Display'] = NumClimbPos1
            rsCEA['Match11Value'] = NumClimbPos1

            rsCEA['Match12Display'] = NumClimbPos2
            rsCEA['Match12Value'] = NumClimbPos2

            rsCEA['Summary1Display'] = NumClimbPos3
            rsCEA['Summary1Value'] = NumClimbPos3

            rsCEA['Summary2Display'] = NumClimbPos4
            rsCEA['Summary2Value'] = NumClimbPos4

            rsCEA['Summary3Display'] = NumClimbPos5
            rsCEA['Summary3Value'] = NumClimbPos5

    return rsCEA
