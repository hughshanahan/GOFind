#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  readXML.py
#  
#  Copyright 2016 Hugh Shanahan <hugh.shanahan@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import sys, xmltodict

def searchEntry(entryData,key):
	found = False
	i = 0
	value = ''
	while (not found):
		try: 
			if (entryData[u'name'][i][u'@type'] == key):
				value = entryData[u'name'][i]['#text']
				found = True
			break
		except KeyError:
			print entryData
			
		i += 1
		if ( i >= len(entryData[u'name']) ):
			found = True
					 
	return value	 
	

def main():
	
	with open('www.uniprot.org.xml') as fd:
		doc = xmltodict.parse(fd.read())
	uniProt = doc[u'uniprot']
	entries = uniProt[u'entry']
	for entry in entries:
		species = searchEntry(entry[u'organism'],u'scientific')
		locus = searchEntry(entry[u'gene'],u'ordered locus')
		print species+' '+locus	

	return 0

if __name__ == '__main__':
	main()

