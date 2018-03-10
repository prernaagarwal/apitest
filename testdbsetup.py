#!/usr/bin/python
# -*- coding: utf-8 -*-
#Setting up psycopg2 and postgresql


import psycopg2

con = None

try:
    con = psycopg2.connect("host='localhost' dbname='pincodes' user='postgres' password='password'")
    print("Connected")
except:
    print ("I am unable to connect to the database")
