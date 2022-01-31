# Script to populate the BlueAllianceTeams table for testing purposes. This would normally be populated by the
# BA script TeamList.py, but before the season this script can be run to fake an event with CT teams.
INSERT INTO BlueAllianceTeams (Team, TeamName, TeamLocation)
SELECT Team, TeamName, TeamLocation FROM Teams
WHERE TeamStateProv='Connecticut';



