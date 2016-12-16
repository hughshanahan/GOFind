#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  NCBIGO.py
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

import GOFind, logging, threading

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s',
                    )
                    
class Abstract2GO(object):
    def __init__(self, NCBIGOs={}):
		self.lock = threading.Lock()
		self.value = NCBIGOs

    def addGOs(self,GOs):
       i = 0		
       logging.debug('Waiting for lock')
       self.lock.acquire()
       try:
           logging.debug('Acquired lock')
           while i in self.value:
			   i += 1
			   
           self.value[i] = GOs
       finally:
           self.lock.release()
           
    def storeGOs(jsonFn):
		with open(jsonFn,'w') as outfile:
			json.dump(self.value,outfile)       
           
def worker(a2g,abstract):
	GOs = GOFind.setSearchTerm(abstract)
	a2g.addGOs(GOs)
	logging.debug('Done')
  

    
def main(args):
	import pubmedQuery
	
	abstracts = pubmedQuery.abstracts(sys.argv[1])
	
	abstract2GO = Abstract2GO()
	
	threads = []
	for a in abstracts:
		t = threading.Thread(target=worker,args=(abstract2GO, a))
		threads.append(t)
		t.start()
		
	threadsAtWork = 1
	
	while (threadsAtWork):
		threadsAtWork = 0
		for t in threads:
			if t.isAlive():
	
				threadsAtWork += 1
	
	abstract2GO.storeGOs(sys.argv[2])
	return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
