This assumes we are running on Ubuntu - not the Pi

The cron job will run the run-analysis.sh script which runs:
	BA/Oprs.py
	BA/Ranks.py
	analysisIR.py
	graphIR.py
	
The top line in run-analysis.sh is /usr/bin/bash on Ubuntu. It is different on the Pi
so I am making a note here to check if there is an issue as something to check

NOTE: when using "crontab -l" you must be pi to see the cron jobs. If you are root
		you will see root's cron jobs which there should be none.

Logon Instructions:
1.	login to pi@markdev20.nmrbox.org
2.	crontab -l  (should be empty)
3.	sudo -i (will log you in as root)
4.	cd /home/pi/scouting_python_2022
5.	./cron-service.sh start
6.	exit (log out of root)
7.	crontab -l (should now show the cron job)

To view the log file to be sure there are no errors ...
1.	cd ~
2.	more analysis.log  (use spacebar to scroll)
or
2.	tail -n 20 analysis.log (will show the last 20 lines)

Stop cron job
1.	sudo -i
2.	cd /home/pi/scouting_python_2022
3. 	./cron-service.sh stop
4.	exit  (log out of root)


Here is what the crontab -l will show:
*/2 * * * * cd /home/pi && /home/pi/scouting_python_2022/run-analysis.sh >> /home/pi/analysis.log 2>&1
The */2 says run every two minutes. Change the 2 to any value that makes sense.
To edit the cron job while running use:
crontab -e
	This will open a vi editor
arrow key over to the #
"x" (will delete the value)
"i" (will start insert mode)
type new number
hit esc (exit edit mode)
while holding shift key press ZZ  (will save and exit the vi editor)

That's all folks!