#!/usr/bin/env python
# edit: wenyang
#
# coding:utf-8
import os
import time
import sys
from multiprocessing import Process
import ConfigParser
from dbconn import rule_exist, get_desc
from alert import lx_alert
from alertsend import smsSend,postInfo
import hashlib
ISOTIMEFORMAT = '%Y-%m-%d'


number = [
    "18310531588",  # zt
    "18611088870",  # fwy
    "18611179855",  # gj
    "18612668657",  # zh
    "18600399904",  # x
]


def hash_msg_id(hashmsg):
    hashid = hashlib.md5(hashmsg).hexdigest()[8:-8]
    return hashid



def set_redis_log(host, items, timeline, itemstatus, itemtype, itemvalue, itemname):
    sqlog = open('msq_dashboard-log.log', 'a+')
    today = time.strftime(ISOTIMEFORMAT, time.localtime())
    now = today + " " + timeline
    if itemstatus == "1":
        msg = "[RECOVER][" + itemtype + "]" + now + "-" + host + \
            "-" + itemname + ":change status to " + itemvalue
    else:
        msg = "[WARNING][" + itemtype + "]" + now + "-" + host + \
            "-" + itemname + ":change status to " + itemvalue
    print >>sqlog, now, msg
    sqlog.close()


def alert_filter(timeline, host, itemname, itemtype, itemstatus, itemvalue, db_ip, db_user, db_pass):
    payload = {}

    sendsw = 0
    today = time.strftime(ISOTIMEFORMAT, time.localtime())
    logfile = open('alertmsg-log.log', 'a+')

    if itemtype in ['SYSLOG', 'OSPF']:
        res = rule_exist(host, itemname, db_ip, db_user, db_pass)
        print res
        if res:
            portdesc = get_desc(host, itemname, db_ip, db_user, db_pass)
            if itemstatus == "1":
                msg = "[RECOVER][" + itemtype + "]" + timeline + "-" + host + \
                    "-" + itemname + ":" + itemvalue + "(" + portdesc + ")"
            else:
                msg = "[WARNING][" + itemtype + "]" + timeline + "-" + host + \
                    "-" + itemname + ":" + itemvalue + "(" + portdesc + ")"

            # log syslog msg which in database whatever alertoff or not

            now = today + " " + timeline
            print >>logfile, now, msg

            if res[0][0] == '0':
                sendsw = 1

    else:
        sendsw = 1
        if itemstatus == "1":
            msg = "[RECOVER][" + itemtype + "]" + timeline + \
                "-" + host + "-" + itemname + ":" + itemvalue
        else:
            msg = "[WARNING][" + itemtype + "]" + timeline + \
                "-" + host + "-" + itemname + ":" + itemvalue

    if sendsw == 1:
        payload['alertstatus'] = itemvalue
        payload['statuscode'] = itemstatus
        payload['messageid'] = hash_msg_id(host+itemname)
        payload['alertitem'] = itemname
        payload['alerttime'] = timeline
        payload['alerthost'] = host
        payload['alertmsg'] = msg
        for idcteam in number:
            smsSend(idcteam, msg)
        postInfo(payload)
        lx_alert(msg)

    logfile.close()


def main():

    # define a list for store msg
    a = []

    # read db config file
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
    items = itemname + "." + itemtype
# refresh dashboard and determine if send alert or not
    p1 = Process(target=set_redis_log, args=(host, items, timeline, itemstatus, itemtype, itemvalue, itemname))
    p2 = Process(target=alert_filter, args=(timeline, host, itemname,itemtype, itemstatus, itemvalue, db_ip, db_user, db_pass))
    p1.start()
    p2.start()
  #  p1.join()
    p2.join()  # block process, alert first , log process wait
if __name__ == '__main__':

    main()
