#!/usr/bin/env python
#edit: wenyang
#
# -*- coding: utf-8 -*-
# encoding: utf-8
#!/usr/bin/python

import MySQLdb
import time
ISOTIMEFORMAT='%Y-%m-%d'
today = time.strftime(ISOTIMEFORMAT,time.localtime())

def rule_exist(hostname,itemname,db_ip,db_user,db_pass):

    db = MySQLdb.connect(db_ip,db_user,db_pass,"enigma" )
    cursor = db.cursor()

    sql = "select Alertoff from  alert_rule where Hostname='"+hostname+"' and Itemname='"+itemname+"'"

  #  sql=sql_base+sql_body
    try:

        #results = cursor.execute(sql)
        cursor.execute(sql)
    results = cursor.fetchall()
        if results:
            return results
        else:
            return False
    except:
        print "Error: unable to fecth data"
    db.close()

def get_desc(hostname,itemname,db_ip,db_user,db_pass)):

    db = MySQLdb.connect(db_ip,db_user,db_pass,"enigma" )
    cursor = db.cursor()

    sql = "select Portdesc from  alert_rule where Hostname='"+hostname+"' and Itemname='"+itemname+"'"

  #  sql=sql_base+sql_body
    try:

        #results = cursor.execute(sql)
        cursor.execute(sql)
        results = cursor.fetchall()
        if results:
            return results[0][0]
        else:
            return False
    except:
        print "Error: unable to fecth data"
    db.close()
