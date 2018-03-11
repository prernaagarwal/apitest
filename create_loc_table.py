#!/usr/bin/python
# -*- coding: utf-8 -*-
 
"""
this file creates the loc table in pincodes database for stages 1 and 2
"""
import csv, psycopg2
import sys
  
   
con = None
    
try:
    con = psycopg2.connect("host='localhost' dbname='pincodes' user='postgres' password='password'")   
    cur = con.cursor()
    cur.execute('CREATE EXTENSION cube');
    cur.execute('CREATE EXTENSION earthdistance');
    cur.execute("CREATE TABLE loc(key TEXT PRIMARY KEY NOT NULL, place_name VARCHAR(100) NOT NULL, admin_name1 VARCHAR(100) NOT NULL, latitude DOUBLE PRECISION, longitude DOUBLE PRECISION, accuracy INT)")

   # with open('/home/prerna/IN.csv', 'r') as file:
   #     reader = csv.reader(file)
   #     next(file)
   #     cur.copy_from(file, 'loc', sep=',', columns=('key','place_name','admin_name1','latitude','longitude','accuracy'))
    
    cur.execute("COPY loc(key, place_name, admin_name1,latitude,longitude,accuracy) FROM '/home/prerna/locations/IN.csv' DELIMITER ',' CSV HEADER")
    con.commit()
except psycopg2.DatabaseError, e:
    if con:
        con.rollback()
    print 'Error %s' % e    
    sys.exit(1)
                                  
finally:   
    if con:
        con.close()
