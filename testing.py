#!/usr/bin/python
from flask import Flask, request, jsonify
import json
from myapp import app
import unittest
import psycopg2
from flask_testing import TestCase
app.testing = True


# Testing /post_location

class MyTest(unittest.TestCase):
	con = None
	cursor = None

	def setUp(self):
		app = Flask(__name__)
		app.config['TESTING'] = True
		app.config['WTF_CSRF_ENABLED'] = False
		self.con, self.cursor = database_setUp()
		return app
	

    #Test1: pincode type is not a string
	def test_pincode_type(self):
		with app.test_client() as client:
			sent = {"pincode" : 110026,"place": "Punjabi Bagh","city": "New Delhi","latitude": 28.6488,"longitude":77.1726, "accuracy": 0}
			sent = json.dumps(sent)
			result = client.post('http://localhost:5000/post_location', data = sent, content_type = 'application/json')
			print(result.data)
			self.assertEqual(result.data, "pincode is not a string")
    
    #Test2: place type is not a string
	def test_place_type(self):
		with app.test_client() as client:
			sent = {"pincode" : "110026","place": 5.0,"city": "New Delhi","latitude": 28.6488,"longitude":77.1726, "accuracy": 0}
			sent = json.dumps(sent)
			result = client.post('http://localhost:5000/post_location', data = sent, content_type = 'application/json')
			print(result.data)
			self.assertEqual(result.data, "place is not a string")
    
    #Test3: city type is not a string
	def test_city_type(self):
		with app.test_client() as client:
			sent = {"pincode" : "110026","place": "Punjabi Bagh","city": 0,"latitude": 28.6488,"longitude":77.1726, "accuracy": 0}
			sent = json.dumps(sent)
			result = client.post('http://localhost:5000/post_location', data = sent, content_type = 'application/json')
			print(result.data)
			self.assertEqual(result.data, "city is not a string")
	
	#Test4: latitude type is not a float
	def test_lat_type1(self):
		with app.test_client() as client:
			sent = {"pincode" : "110026","place": "Punjabi Bagh","city": "New Delhi","latitude": 28,"longitude":77.1726, "accuracy": 0}
			sent = json.dumps(sent)
			result = client.post('http://localhost:5000/post_location', data = sent, content_type = 'application/json')
			print(result.data)
			self.assertEqual(result.data, "latitude is not a float")
	
	#Test5: latitude type is not a float
	def test_lat_type2(self):
		with app.test_client() as client:
			sent = {"pincode" : "110026","place": "Punjabi Bagh","city": "New Delhi","latitude": "hello","longitude":77.1726, "accuracy": 0}
			sent = json.dumps(sent)
			result = client.post('http://localhost:5000/post_location', data = sent, content_type = 'application/json')
			print(result.data)
			self.assertEqual(result.data, "latitude is not a float")

    #Test6: longitude type is not a float
	def test_lon_type1(self):
		with app.test_client() as client:
			sent = {"pincode" : "110026","place": "Punjabi Bagh","city": "New Delhi","latitude": 28.6488,"longitude": 77, "accuracy": 0}
			sent = json.dumps(sent)
			result = client.post('http://localhost:5000/post_location', data = sent, content_type = 'application/json')
			print(result.data)
			self.assertEqual(result.data, "longitude is not a float")

    #Test7: longitude type is not a float
	def test_long_type2(self):
		with app.test_client() as client:
			sent = {"pincode" : "110026","place": "Punjabi Bagh","city": "New Delhi","latitude": 28.6488,"longitude":"hello", "accuracy": 0}
			sent = json.dumps(sent)
			result = client.post('http://localhost:5000/post_location', data = sent, content_type = 'application/json')
			print(result.data)
			self.assertEqual(result.data, "longitude is not a float")

    #Test8: place wth same pincode already exists in the database
	def test_existing_pincode(self):
		with app.test_client() as client:
			sent = {"pincode" : "IN/110026","place": "Punjabi Bagh","city": "New Delhi","latitude": 28.6488,"longitude":77.1726, "accuracy": 0}
			sent = json.dumps(sent)
			result = client.post('http://localhost:5000/post_location', data = sent, content_type = 'application/json')
			print (result.data)
			self.assertEqual(result.data, "place with the same pincode exists")

    #Test9: place with different pincode but same coordinates exist
	def test_same_lat_lon(self):
		with app.test_client() as client:
			sent = {"pincode" : "IN/111111","place": "Punjabi Bagh","city": "New Delhi","latitude": 28.6488,"longitude":77.1726, "accuracy": 0}
			sent = json.dumps(sent)
			result = client.post('http://localhost:5000/post_location', data = sent, content_type = 'application/json')
			print (result.data)
			self.assertEqual(result.data, "place with similar coordinates exists")
    
    #Test10: different pincode but coordinates are close enough be same 
	def test_similar_coordinates(self):
		with app.test_client() as client:
			sent = {"pincode" : "IN/110334","place": "Bharat Nagar","city": "New Delhi","latitude": 28.6400,"longitude": 77.2150, "accuracy": 0}
			sent = json.dumps(sent)
			client.post('http://localhost:5000/delete_post_location', data = sent, content_type = 'application/json') #Delete the test entry if it exists
			result = client.post('http://localhost:5000/post_location', data = sent, content_type = 'application/json') #Add test entry
			print (result.data)
			client.post('http://localhost:5000/delete_post_location', data = sent, content_type = 'application/json') #Delete the test entry if it exists
			self.assertEqual(result.data, "place with similar coordinates exists")

    #Test11: Add an entry to the database
	def test_add_location(self):
		with app.test_client() as client:
			sent = {"pincode" : "IN/500052","place": "Hasannagar","city": "Telangana","latitude": 17.387140,"longitude":78.491684, "accuracy": 0}
			sent = json.dumps(sent)
			client.post('http://localhost:5000/delete_post_location', data = sent, content_type = 'application/json') #Delete the test entry if it exists
			result = client.post('http://localhost:5000/post_location', data = sent, content_type = 'application/json') #Add test entry
			print (result.data)
			client.post('http://localhost:5000/delete_post_location', data = sent, content_type = 'application/json') #Delete the test entry if it exists
			self.assertEqual(result.data, "location saved")

	def tearDown(self):
		self.cursor.close()
		self.con.close()

def database_setUp():
	con = None
	cursor = None
	try:
		con = psycopg2.connect("host='localhost' dbname='pincodes' user='postgres' password='password'")
		cursor = con.cursor()
		#cursor.execute('DELETE FROM loc WHERE key = "IN/500052"')
	except:
		print ("I am unable to connect to the database")
	return con, cursor
    
if __name__ == "__main__":
	

	unittest.main()

	cursor.close()
	con.close()
