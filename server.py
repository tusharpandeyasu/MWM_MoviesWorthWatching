__author__ = 'hacker'
import time
import BaseHTTPServer
import sparql
from urlparse import urlparse

HOST_NAME = 'localhost' # !!!REMEMBER TO CHANGE THIS!!!
PORT_NUMBER = 9000 # Maybe set this to 9000.


class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/hl")
        s.end_headers()
    def do_GET(s):
        """Respond to a GET request."""

        if s.path == '/':
            s.renderTemplate("static/search.html",{})
        elif s.path == '/allMovies/':
            s.renderTemplate("static/AllMovies.html",s.getAllMovies())
        elif '/search/' in s.path:
            query = urlparse(s.path).query
            query_components = dict(qc.split("=") for qc in query.split("&"))
            movieName = query_components['movieName']
            movieName = movieName.replace('%20',' ')
            s.renderTemplate("static/result.html",s.getResultDict(movieName))


    def do_POST(s):
        rawPost = s.rfile.read(int(s.headers.getheader('Content-Length')))
        if s.path == '/search/':
            rawPost = rawPost.split("=")
            rawPost = rawPost[1]
            rawPost=rawPost.replace("+"," ")
            s.renderTemplate("static/result.html",s.getResultDict(rawPost))
        elif s.path == '/allMovies/':
            s.renderTemplate("static/AllMovies.html",s.getAllMovies())

    def getResultDict(s, movieName):
        print movieName
        resultDict = {}

        omdb = sparql.getOmdb(movieName)
        resultDict['mname'] = omdb[0]
        resultDict['myear'] = omdb[1]
        resultDict['mactors'] = omdb[2]
        resultDict['mdir'] = omdb[3]
        resultDict['mgenre'] = omdb[4]
        resultDict['mawards'] = omdb[5]
        resultDict['mrating'] = omdb[6]
        resultDict['mlength'] = omdb[7]
        resultDict['mdate'] = omdb[8]
        resultDict['mcountry'] = omdb[9]
        resultDict['mlanguage'] = omdb[10]
        resultDict['mimg'] = omdb[len(omdb) -2]


        critique = sparql.getCritique(movieName)
        resultDict['cname'] = critique[1]
        resultDict['creview'] = critique[2]

        directors = sparql.getDirectors(movieName)
        resultDict['dname'] = directors[1]
        resultDict['dmovies'] = directors[2]

        tweets = sparql.getTweets(movieName)
        if tweets:
            resultDict['tweets'] = tweets.encode('utf-8')
        else:
            resultDict['tweets'] = 'No tweets could be found for this movie'
        return resultDict

    def getAllMovies(s):
        resultDict = {}
        resultDict['movies'] = sparql.getAllMovies()
        return resultDict

    def renderTemplate(s,templateName, renderDict):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        templateFile = open(templateName).read()
        for key in renderDict.keys():
            replacePattern = "{{"+key+"}}"
            templateFile = templateFile.replace(replacePattern,renderDict[key])
        s.wfile.write(templateFile)



if __name__ == '__main__':
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)