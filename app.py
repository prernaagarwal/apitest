#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Contains API for stages 1 and 2
"""

from flask import Flask, json, request
from location1 import Location
from point import Point1
import psycopg2
#import unittest

app = Flask(__name__)

con = None

#connect to the database
try:
    con = psycopg2.connect("host='localhost' dbname='pincodes' user='postgres' password='password'")
    cursor = con.cursor()
    print("Connected")
except:
    print ("I am unable to connect to the database")

@app.route('/')
def index():
    return "Hello, World!"


"""
Get : Given a location, fetch all the nearby pin codes within a radius. For example, I can ask - give me all points within 5km radius
of (45.12, 71.12) .Using postgres "earthdistance" to compute all points in 5km radius. This api will be /get_using_postgres
"""

@app.route('/get_using_postgres', methods=['GET'])
def get_location():
        lat = float(request.args.get('lat1'))         # get data from the url
        lon = float(request.args.get('lon1'))
        radius = float(request.args.get('distance'))
        p = Point1(lat, lon, radius * 1000) # assumption: radius was given in km, converting it to m
        print(lat,lon,radius)
        return distance(p)

def distance(p):                #calculate distance between two points using earthdistance extension
    cursor.execute("""
                SELECT * FROM loc WHERE gc_to_sec(earth_distance(ll_to_earth(%(lat)s,%(lon)s),
                ll_to_earth(loc.latitude,loc.longitude)))
                <= %(distance)s
                """, 
                {
                    "lat":p.lat1,
                    "lon": p.long1,
                    "distance":p.distance
                }
                )
    nearby_pincodes = cursor.fetchall()
    pincodes_list = []
    for pin in nearby_pincodes:
        pincodes_list.append(pin[0])            #list of all the pincodes that fall within the given distance of the given point

    # print(pincodes_list)

    return json.dumps(pincodes_list)




"""
Get : Given a location, fetch all the nearby pin codes within a radius. For example, I can ask - give me all points within 5km radius
of (45.12, 71.12) . Implement the mathematical computation yourself. this api will be /get_using_self
"""

@app.route('/get_using_self', methods = ['GET'])
def self_get_location():
    lat = float(request.args.get('lat1'))                               # get data from the url
    lon = float(request.args.get('lon1'))
    radius = float(request.args.get('distance'))
    p = Point1(lat, lon, radius) #assumption: radius is given in km
    print(lat,lon,radius)
    return self_distance(p)



def self_distance(p):                    #calculate distance between two points using haveresine formula
    
    #https://gist.github.com/carlzulauf/1724506
    # Haversine formula
    # calculates great circle distance between two points
    
    cursor.execute("""
                SELECT * FROM loc WHERE (2 * 6371 * asin(sqrt(sin(radians(loc.latitude-%(lat)s)/2)^2 + sin(radians(loc.longitude-%(lon)s)/2)^2 * 
                cos(radians(%(lat)s)) * cos(radians(loc.latitude))))) <= %(distance)s 
                """,
                {
                    "lat":p.lat1,
                    "lon": p.long1,
                    "distance":p.distance
                }
                )

    self_nearby_pincodes = cursor.fetchall()
    self_pincodes_list = []
    for pin in self_nearby_pincodes:
        self_pincodes_list.append(pin[0])     #list of all the pincodes that fall within the given distance of the given point

    return json.dumps(self_pincodes_list)





"""
Post : Post lat,lng of any location with pin code+address+city and you can add new pin code in db. This api will be /post_location. 
"""

@app.route('/post_location', methods=['POST'])
def add_location():
        content = request.get_json(force=True)              # Get a json object from the body of Postman 
        l = Location(content)  
        if (not exists(l)):
            save_location(l)
            return json.dumps(l.toJSON())
        else:
            return "Entry exists"

def test_add_location(self):
    response = self.post('/post_locatopn', data = json.dumps(dict(pincode = "11190", 
        place= "p", city= "c", latitude= 2830.4, longitude=8, accuracy= 1)), content_type = 'application/json')
    self.assertEqual(response['latitude'], 2830.4)

def save_location(l):                                       # function to add entry to the database
    cursor.execute("""
                INSERT INTO loc(key, place_name, admin_name1, latitude, longitude, accuracy)
                VALUES (%(pincode)s, %(place)s, %(admin)s, %(latitude)s, %(longitude)s, %(accuracy)s)
                """, 
                {
                    "pincode": l.pincode,
                    "place": l.place,
                    "admin": l.city,
                    "latitude": l.lat,
                    "longitude": l.longitude,
                    "accuracy":l.accuracy
                }

                ) 
    con.commit()

    
#def test_save_location():

def exists(l):
    cursor.execute('SELECT key FROM loc WHERE key = %(pincode)s', 
                {
                    "pincode": l.pincode,
                }
                )
    result = cursor.fetchone()                                        #Check if pin code already exists 

    p = Point1(l.lat, l.longitude, 1 * 1000)  #within 1 km
    res = post_location_distance(p)

    if (result is None):
        if (len(res) == 0):
            return False    # does not exit
        else:
            return True     # entry exists
    else:
        return True         # entry exists
 
    #l = Location(content['pincode'], content['place'], content['city'], content['latitude'], content['longitude'], content['accuracy']) 
    #  print(l)

"""
assumption: Within 1 km, pincode should not change
Check if there are existing latitude+longitude THAT ARE CLOSE ENOUGH TO BE THE SAME 
(dont assume that they will exactly be the same.)
"""
def post_location_distance(p):
    cursor.execute("""
                SELECT * FROM loc WHERE gc_to_sec(earth_distance(ll_to_earth(%(lat)s,%(lon)s),
                ll_to_earth(loc.latitude,loc.longitude)))
                <= %(distance)s
                """, 
                {
                    "lat":p.lat1,
                    "lon": p.long1,
                    "distance":p.distance
                }
                )
    nearby_pincodes = cursor.fetchall()
    pincodes_list = []
    for pin in nearby_pincodes:
        pincodes_list.append(pin[0])

    return pincodes_list






if __name__ == '__main__':
    app.run(debug=True)
        
    cursor.close()
    con.close()

