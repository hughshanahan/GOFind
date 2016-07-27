# GOFind
A simple python library to parse GOCat output


Welcome to GOFind!
A Gene Ontology Based Search Engine that links together GO Terms and organism-specific genes via common GO ids.

It uses a combination of The Gene Ontology Categorizer (http://eagl.unige.ch/GOCat) and The Universal Protein Resource (UniProt) (http://www.uniprot.org) in order to retrieve data. The program is able to take in one more multiple GO Terms as initial input and returns a list of GO terms that directly relate to it; their GOid, score and name. Results can be filtered by setting a minimum score. Data can then be submitted to Uniprot to return all relevant gene-names and organism species associated to the GO term's GOid.


HOW IT WORKS:

There are four lists and ten methods that the program can preform. The contents of the lists depend on what order the methods are carried out in.
Any of the four arrays can be called at any time.

- Method 1: setSearchTerm(goTerm) 
This method takes a string as input that should be the initial search term that you want to look up. This method then converts and reformats the data and then sorts it into a collection of dictionaries. The format of each dictionary goes :
{GOid: ---, ExtraInfo: {Score: ---, Name: ---, GoTermType: ---}}
where GoTermType represents the type of GoTerm (Cellular Component, Molecular Function, Biological Process). Each dictionary is then sorted into a list called arrayMainDictGoCat, which this method returns. It is important to note that this method is essential for making this program work. Without it, the list is empty and thus the other methods work so it is best to call this method first before doing anything. It is also worth noting that once this method has been used, then the call arrayMainDictGoCat[n] will return the nth item in the list. This method allows the user to stack multiple search terms and place as much data as they need into the list before submiting it to Uniprot (e.g. the call setSearchTerm("p53") followed by setSearchTerm("p54") results in a list consisting of data from both Go terms)

- Method 2: getId() 
A simple method for returning the contents of the listGOid list. There is also a message given if the list is empty.

- Method 3: getName() 
A simple method for returning the contents of the listName list. There is also a message given if the list is empty.

- Method 4: getScore() 
A simple method for returning the contents of the listScore list. There is also a message given if the list is empty.

- Method 5: getCurrentList() 
Simply returns the contents of arrayMainDictGoCat. There is also a message given if the list is empty.

- Method 6: filterScore(scoreValue)
Takes in a float value and uses it to filter out the items that are currenty in arrayMainDictGoCat. The method iterates through the list and removes any GoTerm that has a score lower than that given (so )

- Method 7: submitOneBySpecies(goid, species)
Takes the current version of arrayMainDictGoCat and submits one of the goids as input as well as a species. This goid will be used to retrieve data from

- Method 8: flush()
As mentioned before, arrayMainDictGoCat has the ability to stack results from the setSearchTerm method. This method then allows the user to completely remove all information and content from the list, thus refreshing the program. 

- Method 9: size() 
Returns the size of the current version of arrayMainDictGoCat.

- Method 10: submitAllBySpecies(species) 
Same as submitOneBySpecies but this time iterates through the current version of arrayMainDictGoCat and returns Uniprot results for all GOids in the list. Again, this method does work but takes a lot of time to process.


HOW TO IMPLEMENT:

This program is in ways a class so it can be added to your program by adding the following code to your program:

import urllib2, json, csv

class GOFind():

arrayMainDictGoCat = []

listGOid = []

listName = []

listScore = []

[copy paste of all the definitions]



Thank you for being interested in my findings,
William Steve Herbosch
2016
