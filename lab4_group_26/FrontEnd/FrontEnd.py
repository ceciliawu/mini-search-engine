# -*- coding: utf-8 -*-
import bottle
import httplib2
__author__ = '1wptjdm'

from bottle import *
import math
from operator import itemgetter
from collections import Counter
from beaker.middleware import SessionMiddleware
import sqlite3 as sql
import os
import json

runLocal =1 #if 1 run on localhost if 0 run on aws
baseURL = 'http://ec2-34-228-142-172.compute-1.amazonaws.com'


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
app = SessionMiddleware(bottle.app(), session_opts) # app is now a replacement of original bottle.app(); if not specified in run() at bottom, default app
scope = 'https://www.googleapis.com/auth/plus.me https://www.googleapis.com/auth/userinfo.email'


"""@route('/home')
def login_page():

    flow = flow_from_clientsecrets("client_secret.json", scope, redirect_uri=redirect_uri_)
    uri = flow.step1_get_authorize_url()
    print "@login:redirecting to google"
    redirect(uri)
    return

@route('/redirect')
def login_done_redirect():
	global redirect_search_uri
	global user_email
	global user_name
	global user_pic
	test=0
	if test ==0:
		code=request.query.get('code','')
		#flow = OAuth2WebServerFlow(client_id=CLIENT_ID,client_secret=CLIENT_SECRET,scope=scope,redirect_uri=redirect_search_uri)
		flow = OAuth2WebServerFlow(client_id=CLIENT_ID,client_secret=CLIENT_SECRET,scope=scope,redirect_uri=redirect_uri_)
		credentials = flow.step2_exchange(code)
		token = credentials.id_token['sub']
		test=1
	http = httplib2.Http()
	http = credentials.authorize(http)

    #get user email
	users_service = build('oauth2','v2',http=http)
	user_document = users_service.userinfo().get().execute()
	user_email = user_document['email']
	user_name = user_document['name']
	user_pic = user_document['picture']

	print "@login/done:user is now logged in, redirect to search page"

	redirect('/')

@route('/logout')
def logout_page():
	global user_email
	global user_name
	global user_pic
	print "@logout:user is being logged out, redirect to google logout page"
	user_email=""
	user_name=""
	user_pic=""
	redirect("/")
	return
"""
def words(text): return re.findall(r'\w+', text.lower())
WORDS = Counter(words(open('words.txt').read()))
@route('/')
def home():
	return bottle.template ('Search_page')



@route('/search', method='GET')
def search_page_post():
	search = request.query.get('keywords')
	equation = search
	try:
		result=eval(equation)
	except:
		search = list(re.sub('\s+', " ", search).lower().split())
		if len(search)==0:
			redirect ('/')
		#grab the keyword from the text input form and redirect to the first page of the keyword
		else:
			search[0]=correction(search[0])
			redirectURLTemp = baseURL+ "/search/" + search[0]
			for x in range(len(search)-1):
				search[x+1]=correction(search[x+1])
				redirectURLTemp += "+" + search[x+1]
			redirectURLTemp +="/1"
			redirect (redirectURLTemp)
	else:		
		redirectURLTemp=baseURL+"/"+equation+"/"+str(result)
		redirect (redirectURLTemp)

@route('/<equation>/<result>', method='GET')
def calculate_result(equation,result):
	return bottle.template ('Equation', equation = equation, result = result)

@route('/search/<searchTerm>/<pageNumber>', method='GET')
def search_page_results(searchTerm,pageNumber):
	ctrlList = []
	urlList = []
	searchTerm = searchTerm.split("+")

	conn = sql.connect('greenLight.db')
	c = conn.cursor()
	searchTermWord=""
	urlData=[]
	for i in range(len(searchTerm)):
		searchTermWord = searchTerm[i]
		ctrlList.append(searchTermWord)
		query="""
		SELECT DOCUMENT_INDEX.DOCUMENT,PAGERANK_SCORE.DOC_SCORE
		FROM DOCUMENT_INDEX,PAGERANK_SCORE,LEXICON,INVERTED_INDEX
		WHERE LEXICON.WORD = "%s"
			AND INVERTED_INDEX.WORD_ID=LEXICON.ID
			AND DOCUMENT_INDEX.ID =INVERTED_INDEX.DOCUMENT_ID
			AND DOCUMENT_INDEX.ID=PAGERANK_SCORE.DOC_ID
		ORDER BY PAGERANK_SCORE.DOC_SCORE DESC
		""" %searchTermWord.lower()
		
		c.execute(query)
		urlData += c.fetchall() #urlData contains the queried URL data from the database
	max_num=5;
	#int 
	urlData=list(set(urlData))
	if len(urlData)<max_num:
		urlList=urlData

	else:
		remainder = len(urlData)%max_num
		for i in range(len(urlData)):
			if i>=((int(pageNumber)*max_num)-max_num) and i<int(pageNumber)*max_num:
				urlList.append(urlData[i])
	currentPageNumber = pageNumber
	totalNumberPage = math.ceil(float(len(urlData))/max_num)
	ctrlList.append(int(totalNumberPage))
	ctrlList.append(currentPageNumber)

	return bottle.template ('Search', ctrlList = ctrlList, urlList = urlList)



#This displays the error page when an invalid URL is typed into the browser
@error(404)
def error404(error):
	return '404 Not Found'






def P(word, N=sum(WORDS.values())): 
    "Probability of `word`."
    return WORDS[word] / N

def correction(word): 
    "Most probable spelling correction for word."
    return max(candidates(word), key=P)

def candidates(word): 
    "Generate possible spelling corrections for word."
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

def known(words): 
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)

def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word): 
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))

#This runs the webserer on host 'localhost' and port 8080. Can be accessed using http://localhost:8080/
#run(host='0.0.0.0', port=80, app=app)



run(host='0.0.0.0', port=80, debug=True)

