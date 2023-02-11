<h1>Python HTTP Youtube Scraper<h1>
<h3>By Sam Brimhall<h3>
<h4>Version: 1.0<h4>
<p>Welcome to my Python Youtube Scraper! It performs one simple task.
This program takes in an HTTP GET request with a youtube channel name and a number. Then it returns data on the top Youtube API search results by the channel found with that name up to the number given.<p>

<h3>INSTALLATION:</h3>
<p>
1: Install Python 3.7+. Required libraries:
- googleapiclient
- http.server
- urllib.parse
- json

2: (optional) Edit youtubeScraper.py to set IP Address and Port. Default is localhost and 8000. You can also change the API key if needed here.

3: Run the program in terminal using 'python3 .\youtubeScraper.py' within the program directory

4: (optional) If you wish to access your instance remotely, forward the set port on your router to your server's IP. Step 2 is required to change the IP if you do this.</p>    
    
<h3>USAGE:<h3>

<h4>Calling the service:</h4>
<p>
The service takes HTTP GET requests in the following form:

    http://<hostaddress>:<port>/search?channelName=<string>&resultCount=<integer>


hostaddress = the IP or domain of the server running this program. Default is localhost

port = the port that the program is listening on. Default is 8000

string = required field for a string that the service will use as query for a Youtube Channel

integer = required field for the number of videos the service will get.

An example of a complete call using the default config:

    http://localhost:8000/search?channelName=MrBeast&resultCount=4

The query above will return the 4 most recent videos on Youtube uploaded by MrBeast.
</p>

<h4>Parsing the Return Data:</h4>

The return data is in the format of a JSON object, with a nested JSON object for each video returned.

Javascript Can interpret these objects with Object.values().
    

Here is a Javascript code snippet that interprets the objects and produces an array of video embed links:

    //separate each video object
      results = Object.values(data);

      //for each video, build an embed link and add it to the page location by id "yf + i"
      for (let i = 0; i < results.length; i++){
        values.push(JSON.parse(JSON.stringify(Object.values(results[i]))));
        vidLinks.push("https://www.youtube.com/embed/"+values[i][1]);

</p>
    <h3>UML Sequence Diagram ofhow the service works:</h3>
    ![youtubeServiceUMLDiagram](https://user-images.githubusercontent.com/20930665/218242762-48c6676f-a723-4a30-ba4a-13951b8d7988.png)

    
