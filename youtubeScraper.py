#Youtube API Key: AIzaSyAfphFV_50VFfTRVzMfw60bgo6wvlNif64
#Backup API Key: AIzaSyBtAVEMKGDkN-CA-BdgzFzswM0slhim568
#3rd key: AIzaSyCuHh8m6dwfPUKoZrzQ0muKSJMM1H1gOk0

# Import Modules
from googleapiclient.discovery import build
from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse
from urllib.parse import parse_qs
import json

hostName = "localhost"
serverPort = 8000

returnCode = 0

youtube = build('youtube', 'v3', 
                developerKey='AIzaSyAfphFV_50VFfTRVzMfw60bgo6wvlNif64')

#callYoutubeApi takes in the server object and parses it for the received request. Then calls the Youtube API to construct a response. Returns the response code and a dictionary string with processed data.
def callYoutubeAPI(self):
        #Process the URL into data
        try:
                urlBreakdown = urlparse(self.path)
                queries = parse_qs(urlBreakdown.query, keep_blank_values=False, strict_parsing=False, encoding='utf-8', errors='replace', max_num_fields=None)
                channelUsername = str(queries['channelName'][0])
                numResults = int(queries['resultCount'][0])
        except:
                return 400, "\{\}"
        
        #Calls to external API and construct data from the results
        try:
                #Run call to youtube API using given username
                channelSearch = youtube.search().list(
                        part="snippet",
                        maxResults=1,
                        q=channelUsername,
                        type='channel'
                ).execute()
                
                #Run call to youtube API to get top n videos 
                Videos_response = youtube.search().list(
                        part="snippet",
                        maxResults=numResults,
                        q=channelUsername,
                        channelId=channelSearch['items'][0]['id']['channelId'],
                        order='date',
                        type='video'
                ).execute()
                
                songDict = {}
                
                for i in range(numResults):
                        songDict[i] = {}
                        songDict[i]['Title'] = Videos_response['items'][i]['snippet']['title']
                        songDict[i]['id'] = Videos_response['items'][i]['id']['videoId']
                                                        
                print(songDict)

        except:
                return 500, "\{\}"
        
        return 200, songDict


#class called whenever server receives a GET request
class MyServer(BaseHTTPRequestHandler): 
        def do_GET(self):
                #call the function to make API call and construct the data
                returnCode, retrievedSongs = callYoutubeAPI(self)
                
                #send response headers using return code from the function
                self.send_response(returnCode)
                self.send_header("Content-type", "application/json")
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                #Send unique response based on returnCode
                if (returnCode == 400):
                        self.wfile.write(bytes("{\n     Bad Request,\n", "utf-8"))
                        self.wfile.write(bytes("     Error: Request must be in the form 'http://<hostname-default-localhost>:<port-default-8000>/search?channelName=<string>&resultCount=<integer>'\n}", "utf-8"))
                elif (returnCode == 500):
                        self.wfile.write(bytes("{\n     Internal Server Error,\n", "utf-8"))
                        self.wfile.write(bytes("     Error: Problem retrieving data from the Youtube API'\n}", "utf-8"))
                elif (returnCode == 200):
                        try:
                                self.wfile.write(bytes(json.dumps(retrievedSongs), "utf-8"))
                        except:
                                self.wfile.write(bytes("Error printing information...", "utf-8"))
                else:
                        self.wfile.write(bytes("Unknown error occured...", "utf-8"))
                
                        
#Run the server
if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")