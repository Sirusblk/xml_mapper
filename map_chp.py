#! /usr/env/python
# map_chp.py
#
# Author:		David McLaren
# Description:	Maps out events for California Highway Patrol incidents.
# ------------------------------------------------------------------------------
import arcpy
import csv
from arcpy import env
from urllib2 import urlopen
from xml.etree import ElementTree
from xml_mapper import Mapper

class CHP_Mapper(Mapper):
	""" Maps out CHP incidents reported. Inherits from Mapper class
		(from xml_mapper.py)

	Attributes:
		records: Stores records of CHP incidents. (Inherited from Mapper class)
	"""
	def __init__(self, url):
		"""Inits CHP_Mapper, letting the parent class take care of it.
		"""
		super(CHP_Mapper, self).__init__('CHP Incidents', url)


	def read_xml(self):
		""" Reads California Highway Patrol incident xml from self.url, storing 
			in a list.
		"""
		connection = urlopen(self.url)
		in_xml = connection.read()
		state = ElementTree.fromstring(in_xml)
		records = []
		record = []

		# Specific to CHP
		# TODO(David) Nested for loops are bad. Change this to be more
		# efficient, possibly use generators.
		for center in state:
			rec_center = center.attrib['ID']

			for dispatch in center:
				rec_dispatch = dispatch.attrib['ID']

				for log in dispatch:
					record = [rec_center, rec_dispatch]

					record.append(log.attrib['ID'])

					log_time = log.find('LogTime').text.strip('"')
					log_type = log.find('LogType').text.strip('"')
					location = log.find('Location').text.strip('"')
					loc_desc = log.find('LocationDesc').text.strip('"')
					area = log.find('Area').text.strip('"')

					record.append(log_time)
					record.append(log_type)
					record.append(location)
					record.append(loc_desc)
					record.append(area)

					latlon = log.find('LATLON').text.strip('"')

					(lat, lon) = latlon.split(':')
					lat = str(lat[:2]) + '.' + str(lat[2:])
					lon = '-' + str(lon[:3]) + '.' + str(lon[3:])

					record.append(lat)
					record.append(lon)
			
					records.append(record)

		self.records = records


def main():
	mapper = CHP_Mapper('http://media.chp.ca.gov/sa_xml/sa.xml')
	mapper.read_xml()

	header = [
				'Center',
				'Dispatch',
				'Log',
				'LogTime',
				'LogType',
				'Location',
				'LocationDesc',
				'Area',
				'Lat',
				'Lon'
			]

	mapper.write_csv('chp_output.csv', header)

	# 4326 is the code for WGS 1984, polar coordinates (-180, 180) & (90, -90)
	mapper.make_xy('H:/Code/xml_mapper/chp_events.lyr', 'chp_output.csv', 'lon', 'lat', 4326)


if __name__ == '__main__':
	main()
