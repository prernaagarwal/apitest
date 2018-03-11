"""
class Location contains all the information about a certain place
"""
class Location(object):

	def __init__(self,content):
		self.pincode = content['pincode']
		self.place = content['place']
		self.city = content['city']
		self.lat = content['latitude']
		self.longitude = content['longitude']
		self.accuracy = content['accuracy'] 
        
 
#	def __str__(self):
#		return 'Pincode'+ self.pin+' Place: '+ self.place+ ' City: '+ self.city+ ' Latitude: '+ str(self.lat)+'Longitude: '+ str(self.longitude) + 'Accuracy: '+ str(self.accuracy)

	def toJSON(self):
		return {'Pincode': self.pincode, 
			'Place': self.place,
			'City':  self.city, 
			'Latitude':self.lat, 
			'Longitude':self.longitude, 
			'Accuracy' : self.accuracy 
			}
