# Van Data Logging Tools


### Start Up on raspberry pi
add the following lines to /etc/rc.local
```
/home/pi/.conda/envs/huey/bin/python /home/pi/projects/van-data-logging/huey-data/logger.py &
exit 0
```
