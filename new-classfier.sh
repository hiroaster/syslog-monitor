#!/bin/sh

ospf_label='OSPF/5/OSPF_NBR_CHG'
syslog_label='IFNET/2/'

#cat demo.txt | while read line
while read line

do


    if [[ $line == "" ]] #blank line
        then
        continue

         #syslog classify config

     elif [[ "$line" =~ "$syslog_label" ]]  #syslog start
         then
         itemtype="SYSLOG"
         date=`echo $line | awk '{print $1,$2,$3}'`
         device=`echo $line | awk '{print $4}'`
         item=`echo $line |sed 's/.*ifName=//g' | sed 's/, AdminStatus.*//g'`
         status=`echo $line | sed 's/.*OperStatus=//g' | sed 's/, Reason=.*//g'`
         if [[ $status == "UP" ]]
         then
         status_value=1
         else
         status_value=0
         fi
          #syslog end

    elif [[ "$line" =~ "$ospf_label" ]] #ospf start
        then
        itemtype="OSPF"
        date=`echo $line | awk '{print $1,$2,$3}'`
        device=`echo $line | awk '{print $5}'`
        item=`echo $line | awk '{print $10}'| sed 's/.*(//g' | sed 's/)//g'`
        status=`echo $line | awk '{print toupper($14)}'|sed 's/\.//g'`
        if [[ $status == "FULL"  ]]
        then
        status_value=1
        else
        status_value=0
        fi
         #ospf end
    else
        continue

    fi
python controller.py $date $device $item $status_value $itemtype $status
#echo $date $device $item $status_value $itemtype $status
#log-alert
done
