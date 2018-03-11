#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
API: Given a latitude/longitude, it will tell which place it falls within from the list of given places
"""
from flask import Flask, json, request
from location1 import Location
from point import Point1
import psycopg2
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

app = Flask(__name__)

con = None

try:                                                        #set up connection to database
    con = psycopg2.connect("host='localhost' dbname='boundaries' user='postgres' password='password'")
    cursor = con.cursor()
    print("Connected")
except:
    print ("I am unable to connect to the database")


@app.route('/')
def index():
    return "Hello, World!"



@app.route('/containing_place', methods=['GET'])            #get latitude and longitude from the url 
def get_place():
        lat =  float(request.args.get('lat1'))
        lon =  float(request.args.get('lon1'))
        p = Point1(lat, lon, 0)
        print(lon,lat)
        return find_place(p)

def find_place(p):
    cursor.execute("SELECT DISTINCT name FROM boundary")    #get names of all the distinct places in the database
    rows = cursor.fetchall()
    list_of_places = []
    for row in rows:
        list_of_places.append(row[0])                       #put them in a list

    for each_place in list_of_places:                       # get all the data related to a particular place (stored in each_place)
        cursor.execute("""
            SELECT * FROM boundary WHERE boundary.name = %(place)s
            """,
            {
                'place' : each_place
            }
            )

        new_rows = cursor.fetchall()                       
        coordinates = []
        for new_row in new_rows:                            # make a list of all the (longitudes,latitudes) of that particular place 
            coordinates.append((new_row[6], new_row[5]))
        
        #https://stackoverflow.com/questions/43892459/check-if-geo-point-is-inside-or-outside-of-polygon-in-python

        polygon = Polygon(coordinates)                       # create a polygon from the boundary latitudes and longitudes
        point = Point(p.long1,p.lat1)

        sample_point = (p.long1,p.lat1)
        for coord in coordinates:                            #check if the given point lies on the boundary
            if coord == sample_point:
                return json.dumps(each_place)
                break  
        
        if(polygon.contains(point)):                           #check if the point lies within the region
            return json.dumps(each_place)  
  
    return json.dumps("The location is not contained within the given cities")   # the given point neither lies on the boundary nor it lies within any place
 
if __name__ == '__main__':
    app.run(debug=True)
    cursor.close()
    con.close()