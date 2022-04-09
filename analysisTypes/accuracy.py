import statistics


def accuracy(analysis, rsRobotMatches):
    # Initialize the rsCEA record set and define variables specific to this function which lie outside the for loop
    rsCEA = {}
    rsCEA['AnalysisTypeID'] = 72
    numberOfMatchesPlayed = 0
    teleAccuracyList = []
    autoAccuracyList = []
    averageAccuracyList = []

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
            autoBallLow = matchResults[analysis.columns.index('AutoBallLow')]
            if autoBallLow is None:
                autoBallLow = 0
            
            autoBallHigh = matchResults[analysis.columns.index('AutoBallHigh')]
            if autoBallHigh is None:
                autoBallHigh = 0
            
            autoBallMiss = matchResults[analysis.columns.index('AutoBallMiss')]
            if autoBallMiss is None:
                autoBallMiss = 0
            
            teleBallLow = matchResults[analysis.columns.index('TeleBallLow')]
            if teleBallLow is None:
                teleBallLow = 0
            
            teleBallHigh = matchResults[analysis.columns.index('TeleBallHigh')]
            if teleBallHigh is None:
                teleBallHigh = 0
            
            teleBallMiss = matchResults[analysis.columns.index('TeleBallMiss')]
            if teleBallMiss is None:
                teleBallMiss = 0

            # Perform some calculations
            numberOfMatchesPlayed += 1
            #print (str(teleBallHigh) + ", " + str(teleBallLow) + ", " + str(teleBallMiss))
            if (teleBallHigh != 0 or teleBallLow != 0 or teleBallMiss !=0):
                teleAccuracy = round((teleBallHigh + teleBallLow)/(teleBallHigh + teleBallLow + teleBallMiss),2)
            else:
                teleAccuracy = 0
            teleAccuracyList.append(teleAccuracy * 100)
            	
            if (autoBallHigh != 0 or autoBallLow != 0 or autoBallMiss !=0):
                autoAccuracy = round((autoBallHigh + autoBallLow)/(autoBallHigh + autoBallLow + autoBallMiss),2)
            else:
                autoAccuracy = 0
            autoAccuracyList.append(autoAccuracy * 100)
                
            averageAccuracy = round((teleAccuracy + autoAccuracy)/2,2)
           
            rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Display'] = str(teleAccuracy)
            rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Value'] = teleAccuracy
            if teleAccuracy >= 0.9:
                rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Format'] = 5
            elif teleAccuracy >= 0.75:
                rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Format'] = 4
            elif teleAccuracy >= 0.50:
                rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Format'] = 3
            elif teleAccuracy >= 0.25:
                rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Format'] = 2
            else:
                rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Format'] = 1

    if numberOfMatchesPlayed > 0:
        rsCEA['Summary1Display'] = round(statistics.mean(teleAccuracyList), 3)
        rsCEA['Summary1Value'] = round(statistics.mean(teleAccuracyList), 3)
        rsCEA['Summary2Display'] = round(statistics.median(teleAccuracyList), 3)
        rsCEA['Summary2Value'] = round(statistics.median(teleAccuracyList), 3)
        # 3 is for rank
        rsCEA['Summary4Display'] = round(statistics.mean(autoAccuracyList), 3)
        rsCEA['Summary4Value'] = round(statistics.mean(autoAccuracyList), 3)

    return rsCEA
