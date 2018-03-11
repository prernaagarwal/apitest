#!/usr/bin/python
import json

data = json.load(open('shapes_copy.json'))
"""
with open ('shapes_copy.json') as file:
	data = json.load(file)
	"""
print(data)