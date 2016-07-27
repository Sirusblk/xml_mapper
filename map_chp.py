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
	""" Maps out CHP incidents reported.

	Attributes:
		Blah blah blah...
	"""
	def __init__(self):
		super(CHP_Mapper, self).__init__()


	def read_xml(self, xml_url):
		""" Reads California Highway Patrol incident xml from xml_url, storing 
			in a list.
		"""
		connection = urlopen(xml_url)
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

					log_time = self.remove_quotes(log.find('LogTime').text)
					log_type = self.remove_quotes(log.find('LogType').text)
					location = self.remove_quotes(log.find('Location').text)
					loc_desc = self.remove_quotes(log.find('LocationDesc').text)
					area = self.remove_quotes(log.find('Area').text)

					record.append(log_time)
					record.append(log_type)
					record.append(location)
					record.append(loc_desc)
					record.append(area)

					latlon = log.find('LATLON').text

					# [1:-1] Removes quotes
					(lat, lon) = latlon[1:-1].split(':')
					lat = str(lat[:2]) + '.' + str(lat[2:])
					lon = '-' + str(lon[:3]) + '.' + str(lon[3:])

					record.append(lat)
					record.append(lon)
			
					records.append(record)

		self.records = records


def main():
	mapper = CHP_Mapper()
	mapper.read_xml('http://media.chp.ca.gov/sa_xml/sa.xml')

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

	# 4326 is the code for WGS 1984
	mapper.make_xy('H:/Code/chp_mapper/chp_events.lyr', 'chp_output.csv', 'lon', 'lat', 4326)


if __name__ == '__main__':
	main()
