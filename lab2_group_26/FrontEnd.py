__author__= 'paariapdoitsue'

import bottle
from bottle import route, get, post, request, response, run, template, static_file

from operator import itemgetter
from collections import Counter, OrderedDict
import re, operator
from beaker.middleware import SessionMiddleware
import oauth2client.client
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import OAuth2WebServerFlow
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
import httplib2
import json

historydict={}
global sortlist
global searchlist
historylist=[]
#import json values
with open("client_secret.json") as json_file:
	client_secrets = json.load(json_file)
	CLIENT_ID = client_secrets["web"]["client_id"]
	CLIENT_SECRET = client_secrets["web"]["client_secret"] 
	SCOPE = client_secrets["web"]["auth_uri"] #"https://accounts.google.com/o/oauth2/auth"
	REDIRECT_URI = client_secrets["web"]["redirect_uris"][0]
	GOOGLE_SCOPE = 'https://www.googleapis.com/auth/plus.me https://www.googleapis.com/auth/userinfo.email'

# Configure the SessionMiddleware
session_opts = {
    'session.type': 'file',
    'session.cookie_expires': 300,
    'session.data_dir': './data',
    'session.auto': True
}
app = SessionMiddleware(bottle.app(), session_opts) # app is now a replacement of original bottle.app(); if not specified in run() at bottom, default app will be run
user_words= {} # users' search history; a dict of dict: <user_email,<word,count>>
user_recent= {} # 10 recently searched words of a user from earlist to lastest; a dict of list: <user_email,[words]>

# Our application asks Google for access to user info
@route('/home')
def home():
    # create a Flow from a clientsecrets file
    flow = flow_from_clientsecrets("client_secret.json", 
            scope=GOOGLE_SCOPE, # https://www.googleapis.com/auth/plus.me
            redirect_uri="http://ec2-34-235-2-173.compute-1.amazonaws.com:80/redirect")
    # generate the Google authorization server URI
    uri = flow.step1_get_authorize_url()
    bottle.redirect(str(uri))

# If user authorizes our application by logging in to their Google account, an onetime authorization code will be attached
# to the query string when the browser is redirected to '/redirect'. The onetime code can be retrieved as GET parameter,
# then used to exchange for an access token
@route('/redirect')
def redirect_page():
    code = request.query.get('code', '') # if code is not granted to us, return empty string
    # create a Flow again to get credentials
    flow = OAuth2WebServerFlow(client_id= CLIENT_ID, 
            client_secret= CLIENT_SECRET,
            scope= GOOGLE_SCOPE, # https://www.googleapis.com/auth/plus.me
            redirect_uri= REDIRECT_URI)
    # exchanges an authorization code for a Credentials object, which holds refresh and access tokens for access to user data
    credentials = flow.step2_exchange(code)

    # apply credentials to an httplib2.Http() object, so any HTTP requests made with this object will be authorized those credentials
    http = httplib2.Http()
    http = credentials.authorize(http)
    
    session = request.environ.get('beaker.session')
    # Get user email, user name and profile pic if they exist
    users_service = build('oauth2', 'v2', http=http) # build(serviceName, version, http=None)
    user_document = users_service.userinfo().get().execute()
    session['email'] = user_document['email']
    if 'name' in user_document: session['name'] = user_document['name']
    if 'picture' in user_document: session['picture'] = user_document['picture']
    
    #if False:""" Google Plus api
    #plus_service = build('plus', 'v1', http=http)
    #people_resource = plus_service.people()
    #people_document = people_resource.get(userId='me').execute()
    #print "Display name: " + people_document['displayName']
    #print "Image URL: " + people_document['image']['url']
    #"""
    session['name'] = user_document['name']
    
    # retrieved all user data we need, now redirect to the page where the user comes from
    bottle.redirect('/')
    
@route('/logout')
def logout():
    session = request.environ.get('beaker.session')
    session.delete()
    # in case user has logged in but user history has been lost when server gets reloaded
    if 'email' in session and session['email'] and session['email'] in user_words:
        # when a user logs out, only leave the 20 most searched words in its history and delete the rest              
        keywords_countdown= sorted(user_words[session['email']].items(), key= lambda word: word[1], reverse=True)
        if len(keywords_countdown)> 20:
            for word,count in keywords_countdown[20:]: 
                del user_words[user_email][word]
            
    session.delete()
    bottle.redirect('/')


cache = {}
logged_in = 'Login'
user_email = ''
username = ''

#default, setup

# each onlick action
@get('/')
def onclick_search():
	# if user hasn't submitted any input or has just completed a search
	if not request.query.get('keywords', ''):
		session = bottle.request.environ.get('beaker.session') # Get the session object from the environ
		user_email= session.setdefault('email', '') # set email to empty string if user not logged in
		keywords_countdown= [] # initialize countdown list    
		recent_list=[]  
		# if user is logged in and there are records of past searches for this user
		if user_email and user_words.has_key(user_email):
			keywords_countdown= user_words[user_email]
			recent_list= user_recent[user_email]
		return template('Search', keywords_countdown= keywords_countdown, recent_list=recent_list, user_email= user_email, session= session)
	# display result page with word counts
	else:
		rawtext = request.query.get('keywords') # to lower case, supposed to be a string
		rawtextlist = list(re.sub('\s+', " ", rawtext).lower().split()) # replaces anything not a lower case by whitespace, remove whitespace 
		
		mydict = {}
		newlist = []
		sortlist = []
		recent_list=[]
		
		keywords_countdown=[]
		session = bottle.request.environ.get('beaker.session')
		limit = 20
		recent_count = 10
		user_email= session.setdefault('email', '') # set email to empty string if user not logged in
	
		if user_email: # if user is logged in
			if not user_words.has_key(user_email): # if no past records for this user
				user_words[user_email]= {} # initialize the dict for this user to store keywords searched--<key:word, value:count> in cookies
				user_recent[user_email]= [] # initialize the list for this user to store 10 most recent words
		# not logged in, count numbers for this query	----------------------------------------------------------
		for key in rawtextlist:
			if mydict.has_key(key):mydict[key]+=1
			else:mydict[key] = 1
		if user_email: #login, recentlist,histogram---------------------------------------------
		# record each new entry
			for key in rawtextlist:
				if historydict.has_key(key):historydict[key]+=1
				else: historydict[key] = 1
				historylist.append(key)
		# we need to sort by occurance
			historydict_rev = sorted(historydict.iteritems(), key=operator.itemgetter(1),reverse=True)
		
		# we need to know how long the history dict is to avoid index collapse	
			historylen = min(len(historydict_rev),limit)	
	
		# transfer to list to get a short list	
			for key, value in historydict_rev:
				val = [key,value]
				sortlist.append(val)
				newlist.append(val)
			keywords_countdown = sortlist[:limit] # need
		#outputTableHTML0 = "<table id=\"results\"> <tr> <td>Recent Searched 10 Words</td></tr>"
		#outputTableHTML1 = "<table id=\"results\"> <tr> <td>Word</td> <td>History Count</td> </tr>"
		#outputTableHTML2 = "Last Query: " + rawtext + " <h2>Search Result</h2><table id=\"results\"> <tr> <td>Word</td> <td>Result Count</td> </tr> "
			
			if len(historylist)>=10:
				recent_list = historylist[-10:] #recent search
			else:
				recent_list = historylist
			user_words[user_email]= keywords_countdown
			user_recent[user_email]= recent_list
		return template('Index',rawtextlist=rawtextlist,mydict=mydict,recent_list=recent_list,keywords_countdown=keywords_countdown,user_email=user_email,session=session)
		# recent search words: display 10 recently searched words, private to users
		#for i in range(len(this_recent)):
		#	outputTableHTML0 += '<tr> <td>%s</td> </tr>' %(recent_list[i])
		# history count,important to test the history length, if haven't reached 20 words yet, will be out of index, private to users
		#if historylen < limit:
		#	for i in range(historylen):
		#		outputTableHTML1 += '<tr> <td>%s</td> <td>%d</td> </tr>' %(keywords_countdown[i][0],keywords_countdown[i][1])
		#else:
		#	for i in range(limit):
		#		outputTableHTML1 += '<tr> <td>%s</td> <td>%d</td> </tr>' %(keywords_countdown[i][0],keywords_countdown[i][1])
		#build the search results, public, this query
		#for i in range(len(mydict)):
		#	outputTableHTML2 +=  '<tr> <td>%s</td> <td>%d</td> </tr>' %(newlist[i][0],newlist[i][1])
	#	return '''
		
#	''' + outputTableHTML0 + outputTableHTML1 + outputTableHTML2
		
		#del newlist[:]
if __name__=="__main__":
	run(app=app,host = '0.0.0.0', port=80, debug=True)
