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

# Note - we are using the NCBI entrez direct command line scripts esearch, efetch and xtract
# these can be downloaded from ftp://ftp.ncbi.nlm.nih.gov/entrez/entrezdirect/
import os, tempfile

def abstracts(queryString):
	
# First call pubmed to pull out abstracts - one line per abstract	
    temp_name = "./"+next(tempfile._get_candidate_names())
    efetchCommand = "esearch -db pubmed -query \""+queryString+"\" | efetch -mode xml -format abstract | xtract -pattern PubmedArticle -block Abstract -element AbstractText>"+temp_name
    os.system(efetchCommand) 
	
# Now call Normalizr (Python 3 - oi vey) to normalise text. 
# Normalised text will overwrite original text.

    normalizeCommand = "/Users/upac004/Python/GOFind-master/normText.py "+ temp_name
    os.system(normalizeCommand)
    
# Now read in file to get each abstract and return a list    	
    theAbstracts = []
    fd = open(temp_name)
    for line in fd:

        
# Remove any special non-ASCII characters
        line = ''.join([i if ord(i) < 128 else '' for i in line]) 
        theAbstracts.append(line)
        
		
    fd.close()	
    os.remove(temp_name)

    return theAbstracts
	



def main(args):
    myAbstracts = abstracts("SATB2 gene function")
#    for abstract in myAbstracts :
#		print abstract

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
