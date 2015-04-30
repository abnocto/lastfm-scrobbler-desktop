import hashlib
import os.path
import shelve
import urllib.request
import webbrowser
import xml.etree.ElementTree as ET


class Scrobbler:	


	@staticmethod
	def authentificateUser():
		Scrobbler._token = Scrobbler._getLastFMToken()
		Scrobbler._confirmToken(Scrobbler._token)	
	

	@staticmethod
	def getSession():
		params = {}
		params["method"] = "auth.getSession"
		params["api_key"] = Scrobbler._apiKey
		params["token"] = Scrobbler._token
		response = Scrobbler._makeRequest(get=True, params=params)		
		session = Scrobbler._parseResponse(xmlString=response, keyWord="session/key")
		Scrobbler._saveSessionKey(session)


	@staticmethod
	def hasUser():
		return os.path.isfile("session.dat")	


	@staticmethod
	def scrobble(data):
		if not Scrobbler._sessionKey:
			Scrobbler._sessionKey = Scrobbler._readSessionKey()
		params = {}
		params["method"] = "track.scrobble"
		params["api_key"] = Scrobbler._apiKey
		params["sk"] = Scrobbler._sessionKey
		params["artist"] = data["artist"]
		params["track"] = data["track"]
		params["timestamp"] = data["timestamp"]
		Scrobbler._makeRequest(get=False, params=params)


	@staticmethod
	def _confirmToken(token):
		webbrowser.open("http://www.last.fm/api/auth/?api_key=" + Scrobbler._apiKey + "&token=" + token)			
			

	@staticmethod	
	def _getLastFMToken():
		params = {}
		params["method"] = "auth.getToken"
		params["api_key"] = Scrobbler._apiKey
		response = Scrobbler._makeRequest(get=True, params=params)	
		token = Scrobbler._parseResponse(xmlString=response, keyWord="token")
		return token


	@staticmethod
	def _makeRequest(get, params):


		def md5(s):
			return hashlib.md5(s.encode("utf-8")).hexdigest()	

			
		def getStringParams(params):
			result = ""
			for i in params:
				result += i	+ "=" + str(params[i]) + "&"
			return result			


		def getApiSignature(params):
			result = ""
			#result is a string "key1value1key2value2..." where keys should be sorted alphabetically (with method name in params)
			for i in sorted(params):
				result += i + str(params[i])
			#in the end of this string should be api secret key
			result += Scrobbler._apiSecret
			#hashed result
			result = md5(result)	
			return "api_sig=" + result		


		stringParams = getStringParams(params)
		signature = getApiSignature(params)

		if (get):
			url = Scrobbler._lastFMServer + "?" + stringParams + signature
			data = None
			headers = Scrobbler._headersGet
		else:
			url = Scrobbler._lastFMServer
			data = (stringParams + signature).encode("utf-8")
			headers = Scrobbler._headersPost


		request = urllib.request.Request(url=url, data=data, headers=headers)		
		response = urllib.request.urlopen(request)
		return response.read().decode("utf-8")


	@staticmethod
	def _parseResponse(xmlString, keyWord):		
		return ET.fromstring(xmlString).find(keyWord).text


	@staticmethod
	def _readSessionKey():
		shelveFile = shelve.open("session")
		session = shelveFile["sessionKey"]
		shelveFile.close()
		return session


	@staticmethod
	def _saveSessionKey(session):
		shelveFile = shelve.open("session")
		shelveFile["sessionKey"] = session
		shelveFile.close()


	_lastFMServer = "http://ws.audioscrobbler.com/2.0/"
	_configFilePath = "config.txt"
	_configFile = open(_configFilePath)
	_apiKey = _configFile.readline().replace("\r","").replace("\n","")
	_apiSecret = _configFile.readline().replace("\r","").replace("\n","")
	_configFile.close()
	_headersGet = {"User-Agent" : "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36"}
	_headersPost = _headersGet.copy()
	_headersPost.update({"Content-Type" : "application/x-www-form-urlencoded;charset=utf-8"})		
	_sessionKey = None		