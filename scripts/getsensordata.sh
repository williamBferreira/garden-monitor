#!/bin/bash

# Add the following line to the /etc/crontab to run every 15 minutes
#  1 15 * * * * /usr/garden-monitor/scripts/getsensordata.sh
#
cd /usr/garden-monitor/
git pull
cd /usr/garden-monitor/programs/
py  get_all_bme280_sensor_data.py
