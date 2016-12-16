#!/usr/bin/env  python3
# -*- coding: utf-8 -*-
#
#  normText.py
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
	
def main(argv):
   from normalizr import Normalizr
   import tempfile
   import shutil

   inputfile = ''
   outputfile = ''
   writeOverInput = 0

   inputfile = sys.argv[1]
   
   if len(sys.argv) > 2:
	   outputfile = sys.argv[2]
   else:
#	   print("Storing to temporary output")
	   outputfile = "./"+next(tempfile._get_candidate_names())
	   writeOverInput = 1
	   	       
   normalizr = Normalizr(language='en')
   fi = open(inputfile)
   fo = open(outputfile,"w")
   for line in fi:
       nline = normalizr.normalize(line)
       fo.write(nline+"\n")
   fi.close()
   fo.close()
    
   if writeOverInput:
#	   print("Moving output to input")
	   shutil.move(outputfile,inputfile)
	    
   return 0

if __name__ == '__main__':
    import sys,getopt
    sys.exit(main(sys.argv))
