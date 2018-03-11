#!/usr/bin/python
import json, psycopg2, sys

data = json.load(open('shapes_copy.json'))

with open ('shapes_copy.json') as file:
	data = json.load(file)

	#print(data)
 
con = None
    
try:
	con = psycopg2.connect("host='localhost' dbname='boundaries' user='postgres' password='password'")   
	cur = con.cursor()
	cur.execute("CREATE TABLE boundary(key SERIAL PRIMARY KEY NOT NULL, name VARCHAR(100) NOT NULL, type VARCHAR(100) NOT NULL, parent VARCHAR(100) NOT NULL, geometry_type VARCHAR(100) NOT NULL, latitude DOUBLE PRECISION, longitude DOUBLE PRECISION)")
	#count = 0;
	for feature in data['features']:
		"""	    
	    print feature['properties']['name']
	    print feature['properties']['type']
	    print feature['properties']['parent']
	    print feature['geometry']['type']
    	"""
		for coordinate in feature['geometry']['coordinates'][0]: 
    		#print "Latitude: ",	coordinate[0], "Longitude: ", 	coordinate[1]
			cur.execute("""
				INSERT into boundary(name, type, parent, geometry_type, latitude, longitude) VALUES 
				(%(place_name)s, %(place_type)s,%(parent_name)s,%(geometry)s,%(lat)s,%(lon)s)
				""",
				{
					'place_name': feature['properties']['name'],
					'place_type': feature['properties']['type'],
					'parent_name':feature['properties']['parent'],
					'geometry':feature['geometry']['type'],
					'lat': coordinate[0],
					'lon':coordinate[1]
				}
   	 			)
	#		count=count+1
		
	#print(count)
   	 	#print " "
   		#print " "

	con.commit()
except psycopg2.DatabaseError, e:
	if con:
		con.rollback()
	print 'Error %s' % e    
	sys.exit(1)
                                  
finally:   
	if con:
		con.close()

 
