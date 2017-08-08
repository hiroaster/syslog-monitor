#!/bin/sh
ps -fe|grep class |grep -v grep
if [ $? -ne 0 ]
then
echo "start process....."
nohup sh /root/syslog-monitor/ironman.sh &
else
echo "runing....."
fi
