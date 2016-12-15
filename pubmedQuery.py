#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  pubmedQuery.py
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

# Note - we are using the NCBI entrez direct command line scripts esearch and efetch
# these can be downloaded from ftp://ftp.ncbi.nlm.nih.gov/entrez/entrezdirect/
import os, tempfile, xmltodict

def abstracts(queryString):
	temp_name = "./"+next(tempfile._get_candidate_names())
	efetchCommand = "esearch -db pubmed -query \""+queryString+"\" | efetch -mode xml -format abstract >"+temp_name
	print efetchCommand
	os.system(efetchCommand) 
	with open(temp_name) as fd:
		doc = xmltodict.parse(fd.read())		
	fd.close()	
		
	articles = doc[u'PubmedArticleSet'][u'PubmedArticle']	
	
	theAbstracts = []
	
	for article in articles:
		theAbstracts.append(article[u'MedlineCitation'][u'Article'][u'Abstract'][u'AbstractText']
)

	return theAbstracts
	
	
		
	
	
	


def main(args):
    myAbstracts = abstracts("SATB gene function")
    for abstract in myAbstracts :
		print abstract

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
