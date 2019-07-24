import urllib.parse
import urllib.request,json
from urllib.error import HTTPError
import base64
class EnvisionManager_https():
    def __init__(self,host,username='admin',password='Cisco#1234',port='443'):
        self.host = host
        self.port = port
        self.Username = username
        self.Password = password
        self.authentication = b'Basic ' + base64.b64encode(self.Username.encode() + b':' + self.Password.encode())
        self.url = "https://{0}:{1}/services/rest/control_restservice".format(self.host,self.port)##Format'https://<EM Server IP>:443'
        self.header = {
                       'accept': 'application/json',
                       'Content-Type':'application/json',
                       'Authorization':self.authentication,
                       }
        self.Opener = urllib.request.build_opener(urllib.request.HTTPBasicAuthHandler())

#Main HTTP Request
    def __requestHTTPResponse(self,dest,data=None,method='GET'):
        req = urllib.request.Request(dest,data=data,headers=self.header,method=method)
        try:
            response = self.Opener.open(req)
            the_page = response.read()
            reply = json.loads(the_page.decode())
            return reply 
        except HTTPError as e:
            print('HTTP Error:',e)


#call below to get all area ID's and name
    def getAllLocations(self):
        dest = "{0}/getAllLocations".format(self.url)
        resp = self.__requestHTTPResponse(dest)
        return resp


#Call below function to get preset details
    def getAreaLevelsForArea(self,areaID):
        dest = "{0}/getAreaLevelsForArea/{1}".format(self.url,areaID)
        resp = self.__requestHTTPResponse(dest)
        return resp


#call below function for lights preset call
    def applyAreaLevel(self,areaID,areaLevel):
        dest = "{0}/applyAreaLevel/{1}/{2}".format(self.url,areaID,areaLevel)
        resp = self.__requestHTTPResponse(dest,data=None,method='PUT')
        if resp:
            return True
        else:
            return False

#call below function to get luminaire level
    def getLuminaireLevelsForArea(self,areaID):
        dest = "{0}/getLuminaireLevelsForArea/{1}".format(self.url,areaID)
        resp = self.__requestHTTPResponse(dest)
        return resp

#call below function to Set luminaire level
    def applyLuminaireLevel(self,areaID,luminaireID,luminairelevel):
        dest = "{0}/applyLuminaireLevel/{1}/{2}/{3}".format(self.url,areaID,luminaireID,luminairelevel)
        resp = self.__requestHTTPResponse(dest,method='PUT')
        return resp
#call below function to know current status of an area
    def getCurrentStatus(self,areaID):
        dest = "{0}/getCurrentStatus/{1}".format(self.url,areaID)
        resp = self.__requestHTTPResponse(dest)
        print(resp)
        return resp
