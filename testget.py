#!/usr/bin/python
from flask import Flask, request, jsonify
import json
from myapp import app
import unittest
import psycopg2
from flask_testing import TestCase
app.testing = True

class MyTest(unittest.TestCase):

	con = None
	cursor = None

	def setUp(self):
		app = Flask(__name__)
		app.config['TESTING'] = True
		app.config['WTF_CSRF_ENABLED'] = False
		self.con, self.cursor = database_setUp()
		return app
	
	def test_add_location(self):
		with app.test_client() as client:
			result1 = client.get('http://localhost:5000/get_using_postgres?lat1=10.777&lon1=8.965&distance=5000')
			result2 = client.get('http://localhost:5000/get_using_self?lat1=10.777&lon1=8.965&distance=5000000')
			print result1.data
			self.assertTrue(result1.data == result2.data)

	def tearDown(self):
		self.cursor.close()
		self.con.close()

	

def database_setUp():
	con = None
	cursor = None
	try:
		con = psycopg2.connect("host='localhost' dbname='pincodes' user='postgres' password='password'")
		cursor = con.cursor()
		print("Connected to db")
	except:
		print ("I am unable to connect to the database")
	return con, cursor
    
if __name__ == "__main__":
	

	unittest.main()

	cursor.close()
	con.close()
