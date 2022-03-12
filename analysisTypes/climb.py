import statistics

def climb(analysis, rsRobotMatches):
    # Initialize the rsCEA record set and define variables specific to this function which lie outside the for loop
    rsCEA = {}
    rsCEA['AnalysisTypeID'] = 30
    numberOfMatchesPlayed = 0
    ClimbPointsList = []

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
            # Status values: 1=no attempt broke, 2= no attempt played D, 3 = no attempt scored, 4=fail, 5=success
            # ClimbString: B=broke down, D=defense, C=scored cargo
            ClimbStatusID = matchResults[analysis.columns.index('ClimbStatusID')]
            if ClimbStatusID == 0:
                ClimbStatusString = "BD"
                ClimbStatusColor = 0
                ClimbStatusScore = 0
            elif ClimbStatusID == 1:
                ClimbStatusString = "Def"
                ClimbStatusColor = 0
                ClimbStatusScore = 0
            elif ClimbStatusID == 2:
                ClimbStatusString = "Cgo"
                ClimbStatusColor = 0
                ClimbStatusScore = 0
            elif ClimbStatusID == 3:
                ClimbStatusString = "0"
                ClimbStatusColor = 1
                ClimbStatusScore = 0
            else:
                ClimbPosition = matchResults[analysis.columns.index('ClimbPosition')]
                if ClimbPosition == 0:
                    ClimbPositionString = "L"
                elif ClimbPosition == 1:
                    ClimbPositionString = "M"
                elif ClimbPosition == 2:
                    ClimbPositionString = "R"
                else:
                    ClimbPositionString = "?"
                ClimbHeight = matchResults[analysis.columns.index('ClimbHeight')]
                if ClimbHeight == 0:
                    ClimbStatusString = "4|{}".format(ClimbPositionString)
                    ClimbStatusColor = 2
                    ClimbStatusScore = 4
                elif ClimbHeight == 1:
                    ClimbStatusString = "6|{}".format(ClimbPositionString)
                    ClimbStatusColor = 3
                    ClimbStatusScore = 6
                elif ClimbHeight == 2:
                    ClimbStatusString = "10|{}".format(ClimbPositionString)
                    ClimbStatusColor = 4
                    ClimbStatusScore = 10
                elif ClimbHeight == 3:
                    ClimbStatusString = "15|{}".format(ClimbPositionString)
                    ClimbStatusColor = 5
                    ClimbStatusScore = 15
                else:
                    ClimbStatusString = "Err"
                    ClimbStatusColor = 7
                    ClimbStatusScore = 888

            # Perform some calculations
            numberOfMatchesPlayed += 1
            ClimbPointsList.append(ClimbStatusScore)

            rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Display'] = str(ClimbStatusString)
            rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Value'] = ClimbStatusScore
            rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Format'] = ClimbStatusColor

    if numberOfMatchesPlayed > 0:
        rsCEA['Summary1Display'] = round(statistics.mean(ClimbPointsList), 1)
        rsCEA['Summary1Value'] = round(statistics.mean(ClimbPointsList), 1)
        rsCEA['Summary2Display'] = statistics.median(ClimbPointsList)
        rsCEA['Summary2Value'] = statistics.median(ClimbPointsList)
        # 3 is rank

    return rsCEA
