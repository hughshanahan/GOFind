#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  searchtermNCBI.py
#  
#  Copyright 2016 Hugh Shanahan <upac004@STF-MC246-001L.local>
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

# The following generates a list of abstracts that match a search query term from pubmed
# It then finds GO terms that get generated from each of these abstracts by querying GOCat

import pubmedQuery, json, GOFind, copy, sys

def searchtermNCBIGO(searchTerm,jsonFn):
	
	
	abstracts = pubmedQuery.abstracts(searchTerm)
	NCBIGO = []
	i = 0
	print len(abstracts)
	for abstract in abstracts:
		print i
		NCBIGO.append( copy.deepcopy(GOFind.setSearchTerm(abstract) ))
		i += 1
		
	with open(jsonFn,'w') as outfile:
		json.dump(NCBIGO,outfile,indent=1)	
		
	return NCBIGO	
		
		
def main():

    GOs = searchtermNCBIGO(sys.argv[1],sys.argv[2])   
     
#    setSearchTerm("ethylene root")
#    print submitAllBySpecies("Arabidopsis thaliana")
    
    
if __name__ == "__main__":
    main()


