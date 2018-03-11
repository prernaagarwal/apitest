#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, json, request
from location1 import Location
from point import Point1
import psycopg2
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

app = Flask(__name__)

con = None

try:
    con = psycopg2.connect("host='localhost' dbname='boundaries' user='postgres' password='password'")
    cursor = con.cursor()
    #print("Connected")
except:
    print ("I am unable to connect to the database")

@app.route('/')
def index():
    return "Hello, World!"



@app.route('/containing_place', methods=['GET'])
def get_place():
        lat =  0
        lon =  77.4143028259277
        p = Point1(lat, lon, 0)
        print(lon,lat)
        return find_place(p)

def find_place(p):
    cursor.execute("SELECT DISTINCT name FROM boundary")
    rows = cursor.fetchall()
    list_of_places = []
    for row in rows:
        list_of_places.append(row[0])

    for each_place in list_of_places:
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
            coordinates.append((new_row[6], new_row[5]))
        
        #https://stackoverflow.com/questions/43892459/check-if-geo-point-is-inside-or-outside-of-polygon-in-python
        polygon = Polygon(coordinates)
        point = Point(p.long1,p.lat1)

        sample_point = (p.long1,p.lat1)
        for coord in coordinates:    #check if point is on the boundary
            if coord == sample_point:
                return json.dumps(each_place)
                break  
        
        if(polygon.contains(point)):
            return json.dumps(each_place)  
    return json.dumps("The location is not contained within given cities")

if __name__ == '__main__':
    get_place()
    app.run(debug=True)
    cursor.close()
    con.close()