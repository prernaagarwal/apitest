#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, json, request
from location1 import Location
from point import Point
from shapely.geometry import MultiPoint
import psycopg2


try:
    con = psycopg2.connect("host='localhost' dbname='boundaries' user='postgres' password='password'")
    cursor = con.cursor()
    print("Connected")
except:
    print ("I am unable to connect to the database")


def get_place():
        lat = 77.0485782623291
        lon = 28.52424696302
        p = Point(lat, lon, 0)
        print(lat,lon)
        return find_place(p)

def find_place(p):
    cursor.execute("SELECT DISTINCT name FROM boundary")
    rows = cursor.fetchall()
    list_of_places = []
    for row in rows:
        list_of_places.append(row[0])
    print(list_of_places)
    print(" ")
    print(" ")

    for each_place in list_of_places:
        print(each_place)
        cursor.execute("""
            SELECT * FROM boundary WHERE boundary.name = %(place)s
            """,
            {
                'place' : each_place
            }
            )
        new_rows = cursor.fetchall()
        coordinates = []
        for new_row in new_rows:
            coordinates.append((new_row[5],new_row[6]))
        print(coordinates) 
        print " "
        poly = MultiPoint(coordinates).convex_hull
        print(poly) 
        print " "
        point = (p.lat1, p.long1)
        print point  
        print " "
        if (poly.contains(point)):
            print(each_place)
            print (" ")
    return each_place

if __name__ == '__main__':
    get_place()
    #app.run(debug=True)
    cursor.close()
    con.close()


