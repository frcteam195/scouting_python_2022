import statistics

def autoPickup(analysis, rsRobotMatches):
    # start = time.time()
    # print("autonomous time:")
    # Initialize the rsCEA record set and define variables specific to this function which lie outside the for loop
    rsCEA = {}
    rsCEA['AnalysisTypeID'] = 2
    
    numberOfMatchesPlayed = 0
    numBallList = []

    # Loop through each match the robot played in.
    for matchResults in rsRobotMatches:
        tmpString = ''
        numBalls = 0
        
        # This is sort of dumb as rsCEA Team and EventID will be overwritten for each match, but easier
        #   to overwite it up to 12 times than to fix at this time.
        rsCEA['Team'] = matchResults[analysis.columns.index('Team')]
        rsCEA['EventID'] = matchResults[analysis.columns.index('EventID')]
        # We are hijacking the starting position to write DNS or UR. This should go to Auto as it will not
        #   likely be displayed on team picker pages.
        autoDidNotShow = matchResults[analysis.columns.index('AutoDidNotShow')]
        scoutingStatus = matchResults[analysis.columns.index('ScoutingStatus')]
        if autoDidNotShow == 1:
            rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Display'] = 'DNS'
        elif scoutingStatus == 2:
            rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Display'] = 'UR'
        else:
        # Retrieve values from the matchResults and set to appropriate variables
            autoBall1 = matchResults[analysis.columns.index('AutoBallPos1')]
            autoBall2 = matchResults[analysis.columns.index('AutoBallPos2')]
            autoBall3 = matchResults[analysis.columns.index('AutoBallPos3')]
            autoBall4 = matchResults[analysis.columns.index('AutoBallPos4')]
            autoBall5 = matchResults[analysis.columns.index('AutoBallPos5')]
            autoBall6 = matchResults[analysis.columns.index('AutoBallPos6')]
            autoBall7 = matchResults[analysis.columns.index('AutoBallPos7')]

            if autoBall1 == 1:
                tmpString = '1'
                numBalls += 1
            if autoBall2 == 1:
                tmpString = tmpString + '2'
                numBalls += 1
            if autoBall3 == 1:
                tmpString = tmpString + '3'
                numBalls += 1
            if autoBall4 == 1:
                tmpString = tmpString + '4'
                numBalls += 1
            if autoBall5 == 1:
                tmpString = tmpString + '5'
                numBalls += 1
            if autoBall6 == 1:
                tmpString = tmpString + '6'
                numBalls += 1
            if autoBall7 == 1:
                tmpString = tmpString + '7'
                numBalls += 1
            
            # if numBalls > 0:
            #     team = matchResults[analysis.columns.index('Team')]
            #     match = matchResults[analysis.columns.index('TeamMatchNo')]
            #     print ("Team = " + str(team) + ", MatchNo = " + str(match) + ', String = ' + tmpString + ", total balls = " + str(numBalls))
            
            numberOfMatchesPlayed += 1
            numBallList.append(numBalls)

            # Create the rsCEA records for Display, Value, and Format
            rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Display'] = str(tmpString)
            rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Value'] = numBalls
            rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Format'] = 0

    # Create summary data
    if numberOfMatchesPlayed > 0:
        rsCEA['Summary1Display'] = round(statistics.mean(numBallList), 1)
        rsCEA['Summary1Value'] = round(statistics.mean(numBallList), 1)
        rsCEA['Summary2Display'] = statistics.median(numBallList)
        rsCEA['Summary2Value'] = statistics.median(numBallList)


    # end = time.time()
    # print(end - start)

    return rsCEA
