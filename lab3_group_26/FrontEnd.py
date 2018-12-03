# -*- coding: utf-8 -*-
import bottle
import httplib2
__author__ = '1wptjdm'

from bottle import *
import math
from operator import itemgetter
from collections import Counter
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import OAuth2Credentials
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
#from googleapiclient.client import *
from beaker.middleware import SessionMiddleware
import sqlite3 as sql
import os
import json

runLocal =1 #if 1 run on localhost if 0 run on aws
#baseURL= ""
baseURL = "http://ec2-34-235-2-173.compute-1.amazonaws.com"

redirect_uri_ = baseURL + "/redirect"
redirect_search_uri = baseURL+ '/search'
redirect_login_done = baseURL + '/login/done'


#con = sql.connect('FrontEnd.db')
#cur = con.cursor()
#cur.execute("CREATE TABLE History(Email TEXT, Word TEXT, Occurance INT)")

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


user_email = ""
user_name = ""
user_pic = ""


@route('/home')
def login_page():

    flow = flow_from_clientsecrets("client_secret.json", scope, redirect_uri=redirect_uri_)
    #flow = flow_from_clientsecrets("client_secrets.json", scope, redirect_uri=redirect_search_uri)
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

@route('/')
def home():
	global user_email
	global user_name
	global user_pic

	return bottle.template ('Search_page', user_email = user_email, user_name=user_name, user_pic=user_pic)



@route('/search', method='GET')
def search_page_post():
	search = request.query.get('keywords')
	search = list(re.sub('\s+', " ", search).lower().split())
	if len(search)==0:
		redirect ('/')
	#grab the keyword from the text input form and redirect to the first page of the keyword
	else:
		redirectURLTemp = baseURL+ "/search/" + search[0]
		for x in range(len(search)-1):
			redirectURLTemp += "+" + search[x+1]
		redirectURLTemp +="/1"
		redirect (redirectURLTemp)

@route('/search/<searchTerm>/<pageNumber>', method='GET')
def search_page_results(searchTerm,pageNumber):
	global user_email
	global user_name
	global user_pic
	ctrlList = []
	urlList = []
	searchTerm = searchTerm.split("+")

	conn = sql.connect('greenLight.db')
	c = conn.cursor()
	searchTermWord=""

	searchTermWord = searchTerm[0]
	query="""
	SELECT DOCUMENT_INDEX.DOCUMENT,PAGERANK_SCORE.DOC_SCORE
	FROM DOCUMENT_INDEX,PAGERANK_SCORE,LEXICON,INVERTED_INDEX
	WHERE LEXICON.WORD = "%s"
	    AND INVERTED_INDEX.WORD_ID=LEXICON.ID
	    AND DOCUMENT_INDEX.ID =INVERTED_INDEX.DOCUMENT_ID
	    AND DOCUMENT_INDEX.ID=PAGERANK_SCORE.DOC_ID
    ORDER BY PAGERANK_SCORE.DOC_SCORE DESC
	""" %searchTermWord.lower()
	max_num=5;
	c.execute(query)
	urlData = c.fetchall() #urlData contains the queried URL data from the database
	int 
	if len(urlData)<max_num:
		urlList=urlData

	else:
		remainder = len(urlData)%max_num
		for i in range(len(urlData)):
			if i>=((int(pageNumber)*max_num)-max_num) and i<int(pageNumber)*max_num:
				urlList.append(urlData[i])
	currentPageNumber = pageNumber
	totalNumberPage = math.ceil(float(len(urlData))/max_num)
	ctrlList.append(searchTermWord)
	ctrlList.append(int(totalNumberPage))
	ctrlList.append(currentPageNumber)

	return bottle.template ('Search', user_email = user_email, user_name=user_name, user_pic=user_pic,ctrlList = ctrlList, urlList = urlList)



#This displays the error page when an invalid URL is typed into the browser
@error(404)
def error404(error):
	return '404 Not Found'

#This runs the webserer on host 'localhost' and port 8080. Can be accessed using http://localhost:8080/
run(host='0.0.0.0', port=80, app=app)



