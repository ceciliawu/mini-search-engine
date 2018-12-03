__author__= 'paariapdoitsue'

from bottle import route, run, request
from operator import itemgetter
from collections import Counter, OrderedDict
import re, operator

#default, setup display the search page using html
@route ('/', method = 'GET')
def search():
    return '''
        <link href="https://fonts.googleapis.com/css?family=Lobster" rel="stylesheet" type="text/css">
		<style>
  		h1 {
    		font-family: Lobster, Monospace;
		    color: green;
		    text-align: center;
  		}
		.title-size {
    		font-size: 100px;
  		}
  		.is-Transformed {   
  			width: 50%;  
 		    margin: auto;  
  			position: absolute;  
		    top: 50%; left: 50%;  
  		-webkit-transform: translate(-50%,-50%);  
      	-ms-transform: translate(-50%,-50%);  
        transform: translate(-50%,-50%);  
		}  
  		input{
    		border: none;
		    padding: 10px;
		    margin: 10px;
		    height: 20px;
    		width: 500px;
		    border:1px solid #eaeaea;
		    outline:none;
		}
		input:hover{
		    border-color: #a0a0a0 #b9b9b9 #b9b9b9 #b9b9b9;
		}
		input:focus{
		    border-color:#4d90fe;
		}

		input[type="submit"] {
		    border-radius: 2px;
		    background: #f2f2f2;
		    border: 1px solid #f2f2f2;
		    color: #757575;
		    cursor: default;
		    font-size: 14px;
		    font-weight: bold;
		    width: 100px;
		    padding: 0 16px;
		    height:36px;
		}
		input[type="submit"]:hover {
		    box-shadow: 0 1px 1px rgba(0,0,0,0.1);
		    background: #f8f8f8;
		    border: 1px solid #c6c6c6;
		    box-shadow: 0 1px 1px rgba(0,0,0,0.1);
		    color: #222;
		}
		.search-div {
			text-align: center;
		}
		</style>
		<div class="is-Transformed">
			<h1 class="title-size">GreenLight</h1>
			<form action = "/" method="post" class="search-form">
				<input type="text" name="keywords" placeholder="Search..">
				<input type="submit" value="Search">
			</form>
		</div>
    '''
# global variable initialization
historydict = {}
sortlist = []
searchlist = []
# each onlick action
@route('/', method='POST')
def onclick_search():
	rawtext = request.forms.get('keywords') # to lower case, supposed to be a string
	rawtextlist = list(re.sub('\s+', " ", rawtext).lower().split()) # replaces anything not a lower case by whitespace, remove whitespace 

	global historydict
	global sortlist
	global searchlist
	mydict = {}
	newlist = []
	# record each new entry
	for key in rawtextlist:
		if historydict.has_key(key):historydict[key]+=1
		else: historydict[key] = 1
		if mydict.has_key(key):mydict[key]+=1
		else:mydict[key] = 1
	# we need to sort by occurance
	historydict_rev = sorted(historydict.iteritems(), key=operator.itemgetter(1),reverse=True)
	limit = 20	
	# we need to know how long the history dict is to avoid index collapse	
	historylen = min(len(historydict_rev),limit)	
	sortlist = []
	# transfer to list to get a short list	
	for key, value in historydict_rev:
		val = [key,value]
		sortlist.append(val)
		newlist.append(val)
	mylist = sortlist[:limit]
	outputTableHTML1 = "<table id=\"results\"> <tr> <td>Word</td> <td>History Count</td> </tr>"
	outputTableHTML2 = "Search for: " + rawtext + " <h2>Search Result</h2><table id=\"results\"> <tr> <td>Word</td> <td>Result Count</td> </tr> "
	# important to test the history length, if haven't reached 20 words yet, will be out of index
	if historylen < limit:
		for i in range(historylen):
			outputTableHTML1 += '<tr> <td>%s</td> <td>%d</td> </tr>' %(mylist[i][0],mylist[i][1])
	else:
		for i in range(limit):
			outputTableHTML1 += '<tr> <td>%s</td> <td>%d</td> </tr>' %(mylist[i][0],mylist[i][1])
	#build the search results
	for i in range(len(mydict)):
		outputTableHTML2 +=  '<tr> <td>%s</td> <td>%d</td> </tr>' %(newlist[i][0],newlist[i][1])
	return '''
		<link href="https://fonts.googleapis.com/css?family=Lobster" rel="stylesheet" type="text/css">
		<style>
		h1 {
			font-family: Lobster, Monospace;
			color: green;
			text-align: center;
		}
		.title-size {
			font-size: 100px;
		}
		.is-Transformed {   
			width: 50%;  
			margin: auto;  
			position: absolute;  
			top: 50%; left: 50%;  
			-webkit-transform: translate(-50%,-50%);  
			-ms-transform: translate(-50%,-50%);  
			transform: translate(-50%,-50%);  
		}  
		input{
			border: none;
			padding: 10px;
			margin: 10px;
			height: 20px;
			width: 500px;
			border:1px solid #eaeaea;
			outline:none;
		}
		input:hover{
			border-color: #a0a0a0 #b9b9b9 #b9b9b9 #b9b9b9;
		}
		input:focus{
			border-color:#4d90fe;
		}
		input[type="submit"] {
			border-radius: 2px;
			background: #f2f2f2;
			border: 1px solid #f2f2f2;
			color: #757575;
			cursor: default;		<h1 class="title-size is-Transformed">GreenLight</h1>
		<form action = "/" method="post" class="search-form is-Transformed">
			<input type="text" name="search" placeholder="Search..">
			<input type="submit" value="Search">
		</form>
			font-size: 14px;
			font-weight: bold;
			width: 100px;
			padding: 0 16px;
			height:36px;
		}
		input[type="submit"]:hover {
			box-shadow: 0 1px 1px rgba(0,0,0,0.1);
			background: #f8f8f8;
			border: 1px solid #c6c6c6;
			box-shadow: 0 1px 1px rgba(0,0,0,0.1);
			color: #222;
		}
		.search-div {
			text-align: center;
		}
		</style>
		<div class="is-Transformed">
			<h1 class="title-size">GreenLight</h1>
			<form action = "/" method="post" class="search-form">
				<input type="text" name="keywords" placeholder="Search..">
				<input type="submit" value="Search">
			</form>
		</div>
	''' + outputTableHTML1 + outputTableHTML2
	del newlist[:]
run(host = 'localhost', port=8080, debug=True)
