#!/usr/bin/env bash

# It is critical that the crontab file be initiall created with crontab -e first
# to get the permissions correct.

# Script to start / stop the analysisIR.py script as a cron job

if [ "$(id -u)" -ne 0 ] ; then
  echo "This script must be run as root or with sudo"
exit 1
fi

if [ -z "$1" ]; then
  echo "You must enter an argument [start] or [stop]"
  echo "Usage: cron-service.sh start|stop"
  exit 1
fi

if [ "$1" != "start" ] && [ "$1" != "stop" ]; then
  echo "'start' and 'stop' are the only valid arguments"
  exit 1
fi

if [ "$1" == start ]; then
  if grep -q run-analysis.sh /var/spool/cron/crontabs/pi
  then
    echo 'It appears that run-analysis.sh is already running as a cron job!'
    echo 'Aborting!'
    exit 1
  else
    echo 'Creating clean log file analysis.log'
    echo 'Adding run-analysis.sh to cron'
    rm -f /home/pi/analysis.log
    touch /home/pi/analysis.log
    chmod a+rw /home/pi/analysis.log
    # NOTE: The cd /home/pi is critical to get the script to run as a cron job even with the explicit paths defined.
    crontab -l -u pi | echo '*/5 * * * * cd /home/pi && /home/pi/scouting_python_2022/run-analysis.sh >> /home/pi/analysis.log 2>&1' | crontab -u pi -
  fi
fi

if [ "$1" == stop ]; then
  if grep -q run-analysis.sh /var/spool/cron/crontabs/pi
  then
    echo 'run-analysis.sh is being removed from cron'
    sed -i '/run-analysis/d' /var/spool/cron/crontabs/pi
  else
    echo 'run-analysis.sh is not currently in cron. Doing nothing!'
    exit 1
  fi
fi
