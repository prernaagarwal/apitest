#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, json, request
from location1 import Location
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

@app.route('/get_location')
def get_location():
        return "Hello, World!"

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
    return cursor.fetchone() is not None
 
 #l = Location(content['pincode'], content['place'], content['city'], content['latitude'], content['longitude'], content['accuracy']) 
        
      #  print(l)


if __name__ == '__main__':
    app.run(debug=True)

    cursor.close()
    con.close()

