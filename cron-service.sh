#!/usr/bin/env bash

# Script to start / stop the analysisIR.py script as a cron job

if [ "$(id -u)" -ne 0 ] ; then
  echo "This script must be run as root or with sudo"
exit 1
fi

if [ -z "$1" ]; then
  echo "You must enter an argument [start] or [stop]"
  echo "Usage: sudo analysis-service.sh start|stop"
fi

if [ "$1" != "start" ] && [ "$1" != "stop" ]; then
  echo "'start' and 'stop' are the only valid arguments"
  exit 1
fi

if [ "$1" == start ]; then
  if grep -q analysis.sh /var/spool/cron/crontabs/mmaciejewski
  then
    echo 'It appears that analysis.sh is already running as a cron job!'
    echo 'Aborting!'
    exit 1
  else
    echo 'Creating clean log file analysis.log'
    echo 'Adding analysis.sh to cron'
    rm -f /tmp/analysis.log
    touch /tmp/analysis.log
    chmod a+rw /tmp/analysis.log
    # NOTE: The cd /home/pi is critical to get the script to run as a cron job even with the explicit paths defined.
    echo '* * * * * cd /home/nmrbox/mmaciejewski && /usr/bin/python3 /home/nmrbox//scouting_python/analysisIR.py >> /tmp/analysisIR.log 2>&1' >> /var/spool/cron/crontabs/pi
  fi
fi

if [ "$1" == stop ]; then
  if grep -q analysisIR /var/spool/cron/crontabs/pi
  then
    echo 'analysisIR.py is being removed from cron'
    sed -i '/analysisIR/d' /var/spool/cron/crontabs/pi
  else
    echo 'analysisIR.py is not currently in cron. Doing nothing!'
    exit 1
  fi
fi
