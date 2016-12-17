# Undergraduate Research Opportunity Project Summer 2016
# Project GOFind
#
# Uses a combination of http://eagl.unige.ch/GOCat and http://www.uniprot.org in order to retrieve data.
# The program takes in a Search Term as input and returns a list of GO terms; their GOid, score and name.
# Results can be filtered by setting a minimum score
# Data can then be submitted to Uniprot to return all relevant gene-names and organism species associated to the GO term's GOid
#
# @author William Steve Herbosch
# @author Hugh Shanahan

#Imports:
# urllib2 needed to read urls and retrieve data from them
# json needed to read json files
# csv needed to read the data from Uniprot 
import urllib2, json, csv, re, sys, xmltodict, tempfile, os
from subprocess import call

arrayMainDictGoCat = []
listGOid = []
listName = []
listScore = []

def initialiseGlobalVariables():
    #Constants:
    #Array that contains all the Terms from GoCat. Items can be added and removed from it.
    arrayMainDictGoCat = []
    #List that contains all GOids of GoTerms
    listGOid = []
    #List that contains all Names of GoTerms
    listName = []
    #List that contains all Scores of GoTerms
    listScore = []

#Method 1: setSearchTerm(goTerm) 
# Takes a search term as input and returns a list of dictionaries containing information about related GO terms
def setSearchTerm(goTerm,searchType='ml'):
    initialiseGlobalVariables()
    searchTypes = ['db','ml','mx']
    if searchType not in searchTypes:
       sys.exit("setSearchTerm:- searchTypes must be db, ml or mx")
	#Create strings
    urlGoCat_part1 = "http://eagl.unige.ch/GOCat/result.jsp?queryTXT="
    urlGoCat_part3 = "%20function&cat="+searchType+"&json"
    #Sets the input value as a string and fixed all " " for "%20", as they usually do in urls
    urlGoCat_part2Temp = str(goTerm)
    urlGoCat_part2 = urlGoCat_part2Temp.replace(' ', '%20')
    urlGoCat_part2 = urlGoCat_part2.replace('/','')
    urlGoCat_part2 = urlGoCat_part2.replace('\t','')
    #Combines all parts of the GoCat url
    urlGoCatFULL = urlGoCat_part1 + urlGoCat_part2 + urlGoCat_part3
    urlGoCatFULL = urlGoCatFULL.replace('\n','')
    #Open the GoCat url
#    print urlGoCatFULL
    webUrlGoCat = urllib2.urlopen(urlGoCatFULL)
    #Standard url code 200 check
    if (webUrlGoCat.getcode() == 200):
        #read the GoCat data
        dataGoCat = webUrlGoCat.read()
        #Collect and convert the JSON file from the GoCat into Python object
        with open('dataGoCat.txt', 'w') as outfile:
            json.dump(dataGoCat, outfile) 
        #String replacement fixes. 
        #Whilst this program was in development, the GoCat API is slightly out-dated format. 
        #It should be fixed now but this is still here just in case.
        dataGoCat2 = dataGoCat.replace('" "score":', '", "score":')
        dataGoCat3 = dataGoCat2.replace('}],}', '}]}')    
        #Convert Python object into String        
        dataGoCatString = str(dataGoCat3)
        #Write dataGoCatString into a JSON file
        fGoCat = open("textGoCat.dat", "w")
        fGoCat.write(dataGoCatString)
        fGoCat.close()
        #Read the file
        fGoCatP = open("textGoCat.dat", "r")
        jsonGoCat = json.load(fGoCatP) 
        #Counter to iterate through the CC part of the JSON file 
        counterCC = 0
        #While loop that iterates through every term
        while (counterCC < len(jsonGoCat["cellular_components"])): 
            #Sets shortcut variables for JSON variables. Also makes 1.0 into 1.00 for decimal placing
            ccGoid = jsonGoCat["cellular_components"][counterCC]["GOid"]
            ccScoreTemp = str(jsonGoCat["cellular_components"][counterCC]["score"])
            ccScore = ccScoreTemp.replace("1.0", "1.00")
            ccName = jsonGoCat["cellular_components"][counterCC]["name"]
            #Adds GOid to list of GOids
            listGOid.append(ccGoid)
            #Adds Name to list of Names
            listName.append(ccName)
            #Adds Score to list of Scores
            listScore.append(ccScore)
            #Creates a sub-dictionary that stores Score, Name and GoTermType
            subDictGoCat = {"Score": ccScore, "Name": ccName, "GoTermType": "Cellular Component"}
            #Creates a directory that stores both GOid and the sub-directory that was just created      
            mainDictGoCat = {"GOid": ccGoid, "ExtraInfo": subDictGoCat}
            #Adds the new directory to a list/array
            arrayMainDictGoCat.append(mainDictGoCat.copy()) 
            #Adds counter to help while loop move to the next item
            counterCC = counterCC + 1        
        #Counter to iterate through the MF part of the JSON file 
        counterMF = 0
        #While loop that iterates through every term
        while (counterMF < len(jsonGoCat["molecular_function"])):    
            #Sets shortcut variables for JSON variables. Also makes 1.0 into 1.00 for decimal placing
            mfGoid = jsonGoCat["molecular_function"][counterMF]["GOid"]
            mfScoreTemp = str(jsonGoCat["molecular_function"][counterMF]["score"])
            mfScore = mfScoreTemp.replace("1.0", "1.00")
            mfName = jsonGoCat["molecular_function"][counterMF]["name"]
            #Adds GOid to list of GOids
            listGOid.append(mfGoid)
            #Adds Name to list of Names
            listName.append(mfName)
            #Adds Score to list of Scores
            listScore.append(mfScore)          
            #Creates a sub-dictionary that stores both Score and Name
            subDictGoCat = {"Score": mfScore, "Name": mfName, "GoTermType": "Molecular Function"}
            #Creates a directory that stores both GOid and the sub-directory that was just created      
            mainDictGoCat = {"GOid": mfGoid, "ExtraInfo": subDictGoCat}
            #Adds the new directory to a list/array
            arrayMainDictGoCat.append(mainDictGoCat.copy()) 
            #Adds counter to help while loop move to the next item
            counterMF = counterMF + 1
        #Counter to iterate through the BP part of the JSON file 
        counterBP = 0
        #While loop that iterates through every term
        while (counterBP < len(jsonGoCat["biological_processes"])): 
            #Sets shortcut variables for JSON variables. Also makes 1.0 into 1.00 for decimal placing
            bpGoid = jsonGoCat["biological_processes"][counterBP]["GOid"]
            bpScoreTemp = str(jsonGoCat["biological_processes"][counterBP]["score"])
            bpScore = bpScoreTemp.replace("1.0", "1.00")        
            bpName = jsonGoCat["biological_processes"][counterBP]["name"]
            #Adds GOid to list of GOids
            listGOid.append(bpGoid)
            #Adds Name to list of Names
            listName.append(bpName)
            #Adds Score to list of Scores
            listScore.append(bpScore)
            #Creates a sub-dictionary that stores both Score and Name
            subDictGoCat = {"Score": bpScore, "Name": bpName, "GoTermType": "Biological Process"}
            #Creates a directory that stores both GOid and the sub-directory that was just created      
            mainDictGoCat = {"GOid": bpGoid, "ExtraInfo": subDictGoCat}
            #Adds the new directory to a list/array
            arrayMainDictGoCat.append(mainDictGoCat.copy()) 
            #Adds counter to help while loop move to the next item
            counterBP = counterBP +1
        #Close Reader
        fGoCatP.close()
        #Returns the list of dictionaries in the format
        # {"ExtraInfo": {"Score": ---, "Name": ---, "GoTermType": ---}, "GOid": ---}
        return arrayMainDictGoCat
    #Else Statement for 200 check    
    else:
        #Error Statement + Error
        return "Error: Could not retrieve results from server" + str(webUrlGoCat.getcode())
   
#Method 2: getID()
# Returns a list of GOids
def getId():
    #If statement checking of list is empty before it prints
    if not listGOid:
        return "List is empty"
    else:
        #Returns the contents of listGOid
        return listGOid

#Method 3: getName()
# Returns a list of Names
def getName():
    #If statement checking of list is empty before it prints
    if not listName:
        return "List is empty"
    else:
        #Returns the contents of listName
        return listName
    
#Method 4: getScore()
# Returns a list of Scores
def getScore(): 
    #If statement checking of list is empty before it prints
    if not listScore:
        return "List is empty"
    else:
        #Returns the contents of listScore
        return listScore

#Method 5: getCurrentList()
# Returns the current version of the list
def getCurrentList():
    #If statement checking of list is empty before it prints
    if not arrayMainDictGoCat:
        return "List is empty"
    else:
        #Returns the contents of listScore
        return arrayMainDictGoCat 

#Method 6: filterScore(scoreValue)
# Filters the list by removing items that have a score below that which is given as input
def filterScore(scoreValue): 
    #Counter
    listCounter = 0
    #While loop to iterate through list
    while (listCounter < len(arrayMainDictGoCat)):
        #If the item's score value is less than the score input
        if (float(arrayMainDictGoCat[listCounter]["ExtraInfo"]["Score"]) < float(scoreValue)):
            #Remove that item from the list
            arrayMainDictGoCat.remove(arrayMainDictGoCat[listCounter])
        else:
            #Else, move to the next item
            listCounter = listCounter + 1

#Method 7. submitOneBySpecies(goid, species)
# Returns a list that contains gene names from a given species that correlate to a given GO id  
def submitOneBySpecies(goid, species):
    #Sets Uniprot urls as strings
    urlUniprot_part1 = "http://www.uniprot.org/uniprot/?query=GO:"
    urlUniprot_part3 = "&&columns=genes,organism&format=tab"
    #Sets the string input from goid
    urlUniprot_part2 = goid
    #Combines all Uniprot url strings to make a single url, including the goid input
    urlUniprotFULL = urlUniprot_part1 + urlUniprot_part2 + urlUniprot_part3
    #Opens and reads the url data via csv
    responce = urllib2.urlopen(urlUniprotFULL)
    csvReader = csv.reader(responce)
    #Creates an array to store the genes
    arrayGeneFilteredFromSpecies = []
    #For loop to read through each line of the data
    for row in csvReader:
        #Converts the current line into a string
        rowString = str(row)
        #Reformatting string to be easily readable
        rowString1 = rowString.replace("['", "")
        rowString2 = rowString1.replace("']", "")
        rowString3 = rowString2.replace('["', '')
        rowString4 = rowString3.replace('"]', '')
        #Separates Genes and Species and assigns them values
        thisIsAGene = rowString4.split("\\t")[0]
        thisIsASpecies = rowString4.split("\\t")[1]
        #Creates a dictionary containing said two values
        dictGeneSpecies = {"Gene": thisIsAGene, "Species": thisIsASpecies}
        #If the Species value in that row contains the string of the species input
        if species in dictGeneSpecies["Species"]:
            #Add that dict to the list
            arrayGeneFilteredFromSpecies.append(dictGeneSpecies["Gene"])
    #Return the list
    return arrayGeneFilteredFromSpecies

# Method 8. flush() 
# Removes all items from the list
def flush():
    #Counter
    counter = 0
    #Go through the list
    while (counter < len(arrayMainDictGoCat)):
        #Remove each item along the way
        arrayMainDictGoCat.remove(arrayMainDictGoCat[counter])
        #Counter
    counter2 = 0
    #Go through the list
    while (counter2 < len(listGOid)):
        #Remove each item along the way
        listGOid.remove(listGOid[counter2])
        #Counter
    counter3 = 0
    #Go through the list
    while (counter3 < len(listName)):
        #Remove each item along the way
        listName.remove(listName[counter3])
        #Counter
    counter4 = 0
    #Go through the list
    while (counter4 < len(listScore)):
        #Remove each item along the way
        listScore.remove(listScore[counter4])
        
# Method 9. size()
# returns the size of the array
def size():
    #return the length of the array
    return len(arrayMainDictGoCat)

# Method 10. submitAllBySpecies(species)
# Same as submitOneBySpecies, but does not ask for a goid as input because it submits all items in the current version of the list
def submitAllBySpecies(species):
    #Creates an array to store the genes
    dictGeneFilteredFromSpecies = {}
    
    #Iterator to go through dict
    for thisGOCat in iter(arrayMainDictGoCat):
        #Sets Uniprot urls as strings
        urlUniprot_part1 = "http://www.uniprot.org/uniprot/?query=go-id:"
        urlUniprot_part3 = "&format=xml"
        #Sets the string input from goid
        urlUniprot_GO = thisGOCat["GOid"]
        scote = thisGOCat["ExtraInfo"]["Score"]
        if ( re.search('^GO\:',urlUniprot_GO) != None ): 
			urlUniprot_GO = urlUniprot_GO.lstrip('GO:')
        urlUniprot_part2 = "%s+AND+species:%s" %(urlUniprot_GO,urllib2.quote(species)) 
        
        #Combines all Uniprot url strings to make a single url for xml, including the goid/species input
        urlUniprotFULL = urlUniprot_part1 + urlUniprot_part2 + urlUniprot_part3
        #Opens and reads the xml data 
        
        temp_name = "./"+next(tempfile._get_candidate_names())
        curlCommand = "curl -L -o "+temp_name+" \""+urlUniprotFULL+"\" >& /dev/null"
        os.system(curlCommand)
        
        if os.stat(temp_name).st_size > 0:
			with open(temp_name) as fd:
				doc = xmltodict.parse(fd.read())
			    
        #Now gather all the genes, remove all spurious species that slip through
			entries = doc[u'uniprot'][u'entry']
			print 'Starting query'
			for entry in entries:
				entrySpecies = searchEntry(entry,u'organism',u'scientific')
				locus = searchEntry(entry,u'gene',u'ordered locus')
				if entrySpecies == species:
  #Creates a dictionary containing said two values				
					dictGeneSpecies = {"Gene": locus, "Species": species}
  #If the Species value in that row contains the string of the species input				
					if species in dictGeneSpecies["Species"]:
  #Add that dict to the list 					
						arrayGeneFilteredFromSpecies.append(dictGeneSpecies["Gene"]) 
						                
        os.remove(temp_name)
    #Return the list
    return arrayGeneFilteredFromSpecies

def searchEntry(entry,rootKey,key):
	found = False
	i = 0
	value = ''
	if rootKey in entry: 
		entryData = entry[rootKey]
		if type(entryData) is dict:
			while (not found):
			
				if type(entryData[u'name']) is list:
					eD = entryData[u'name'][i]
				else:
					eD = entryData[u'name']
		    
				try: 
					if (eD[u'@type'] == key):
						value = eD['#text']
						found = True
						break
				except KeyError:
					print eD

				if ( i >= len(entryData[u'name']) ):
					found = True
			
				i += 1
		   
					 
	return value	 
	

