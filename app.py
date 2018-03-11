#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, json, request
from location1 import Location
from point import Point1
import psycopg2

app = Flask(__name__)

con = None

try:
    con = psycopg2.connect("host='localhost' dbname='pincodes' user='postgres' password='password'")
    cursor = con.cursor()
    print("Connected")
except:
    print ("I am unable to connect to the database")

@app.route('/')
def index():
    return "Hello, World!"




@app.route('/get_using_postgres', methods=['GET'])
def get_location():
        lat = float(request.args.get('lat1'))
        lon = float(request.args.get('lon1'))
        radius = float(request.args.get('distance'))
        p = Point1(lat, lon, radius * 1000) # assumption: radius was given in km, converting it to m
        print(lat,lon,radius)
        return distance(p)

def distance(p):
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

    # print(pincodes_list)

    return json.dumps(pincodes_list)










@app.route('/get_using_self', methods = ['GET'])
def self_get_location():
    lat = float(request.args.get('lat1'))
    lon = float(request.args.get('lon1'))
    radius = float(request.args.get('distance'))
    p = Point1(lat, lon, radius) #assumption: radius is given in km
    print(lat,lon,radius)
    return self_distance(p)



def self_distance(p):
    
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
        self_pincodes_list.append(pin[0])

    return json.dumps(self_pincodes_list)








@app.route('/post_location', methods=['POST'])
def add_location():
        content = request.get_json(force=True)
        l = Location(content)  
        if (not exists(l)):
            save_location(l)
            return json.dumps(l.toJSON())
        else:
            return "Entry exists"

def save_location(l):    
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
    
def exists(l):
    cursor.execute('SELECT key FROM loc WHERE key = %(pincode)s', 
                {
                    "pincode": l.pincode,
                }
                )
    result = cursor.fetchone()
    p = Point1(l.lat, l.longitude, 1.5 * 1000)  #1.5 km
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

