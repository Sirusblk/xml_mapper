#! /usr/env/python
# xml_mapper.py
#
# Author:		David McLaren
# Description:	Maps out events for California Highway Patrol as well as
#				Southern California Edison Outages.
# ------------------------------------------------------------------------------
import arcpy
import csv
from abc import abstractmethod
from arcpy import env
from urllib2 import urlopen
from xml.etree import ElementTree

class Mapper(object):
	""" Maps out CHP events to a point feature class.

	Attributes:
		records: Stores records of CHP incidents.
	"""
	def __init__(self):
		""" Inits Mapper with output file path and dictionary of data"""
		self.records = []


	def remove_quotes(self, text):
		""" Removes quotes from text by shearing off the first and last element
		    of a string.
		"""
		if text != None:
			if text[0:1] is '"':
				return text[1:-1]

		return text


	@abstractmethod
	def read_xml(self):
		""" This is an empty function the children must implement
		"""
		pass


	def write_csv(self, out_file_name, header):
		""" Exports records to .csv file.
		"""

		with open(out_file_name, 'wb') as outf:
			writer = csv.writer(outf, quoting=csv.QUOTE_ALL)
			writer.writerow(header)
			writer.writerows(self.records)
	

	def make_xy(self, save_location, in_table, x_coords, y_coords, sp_ref):
		""" Using ArcPy create a point shapefile.
		"""
		try:
			# Assign Variables
			out_layer = 'events'

			# Create XY Layer (this will not save it)
			arcpy.MakeXYEventLayer_management(in_table, x_coords, y_coords, out_layer, sp_ref)

			# Overwrite the file no matter what
			arcpy.env.overwriteOutput = True

			# Save to layer file
			arcpy.SaveToLayerFile_management(out_layer, save_location)

		except:
			print(arcpy.GetMessages())


def main():
	pass


if __name__ == '__main__':
	main()
