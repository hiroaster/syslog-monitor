#!/usr/bin/env python
#edit: wenyang
#
#coding:utf-8
import os,time
import sys
from multiprocessing import Process
from dbconn import rule_exist,get_desc
from alert import lx_alert
ISOTIMEFORMAT='%Y-%m-%d'


def set_redis_log(host,items,timeline,itemstatus,itemtype,itemvalue,itemname):
    sqlog=open('msq_dashboard-log.log','a+')
    today = time.strftime(ISOTIMEFORMAT,time.localtime())
    now = today+" "+timeline
    if itemstatus == "1":
        msg = "[RECOVER]<"+itemtype+">"+now+"-"+host+"-"+itemname+":change status to "+itemvalue
    else:
        msg = "[WARNING]<"+itemtype+">"+now+"-"+host+"-"+itemname+":change status to "+itemvalue
    print >>sqlog,now,msg
    sqlog.close()




def alert_filter(timeline,host,itemname,itemtype,itemstatus,itemvalue,db_ip,db_user,db_pass):
    res = rule_exist(host,itemname,db_ip,db_user,db_pass)
    print res
    if res:
    portdesc = get_desc(host,itemname,db_ip,db_user,db_pass)
        today = time.strftime(ISOTIMEFORMAT,time.localtime())
        logfile=open('alertmsg-log.log','a+')
        if itemstatus == "1":
            msg = "[RECOVER]<"+itemtype+">"+timeline+"-"+host+"-"+itemname+":"+itemvalue+"("+portdesc+")"
        else:
            msg = "[WARNING]<"+itemtype+">"+timeline+"-"+host+"-"+itemname+":"+itemvalue+"("+portdesc+")"

        #print msg
        now = today+" "+timeline
        print >>logfile,now,msg
        logfile.close()
    if res[0][0] == '0':
        lx_alert(msg)






def main():

    #define a list for store msg
    a=[]

    #read db config file
    cf = ConfigParser.ConfigParser()
    cf.read("db.conf")
    secs = cf.sections()
    if 'db' in secs:
        db_ip = cf.get("db", "db_ip")
        db_user = cf.get("db", "db_user")
        db_pass = cf.get("db", "db_pass")

    else:
        sys.exit()
        
    timeline = sys.argv[3]
    host = sys.argv[4]
    itemname = sys.argv[5]
    itemtype = sys.argv[7]
    itemstatus = sys.argv[6]
    itemvalue = sys.argv[8]
    items = itemname+"."+itemtype
# refresh dashboard and determine if send alert or not
    p1 = Process(target=set_redis_log,args=(host,items,timeline,itemstatus,itemtype,itemvalue,itemname))
    p2 = Process(target=alert_filter,args=(timeline,host,itemname,itemtype,itemstatus,itemvalue,db_ip,db_user,db_pass))
    p1.start()
    p2.start()
  #  p1.join()
    p2.join() #block process, alert first , log process wait
if __name__ == '__main__':

    main()