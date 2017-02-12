__author__ = 'hacker'
import rdflib,re

g = rdflib.Graph()


def getGeneric(query,fileName):
    g.parse(fileName)
    qres = g.query(query)
    if len(qres) > 0:
        return qres
    return None



def getDirectors(movieName):
    query = "select ?IsDirectorOf ?name ?KnownFor ?DTest"\
                + "where { "\
                + "?dirList topMovies:IsDirectorOf '"+ movieName + "'."\
                + "?dirList topMovies:IsDirectorOf ?IsDirectorOf."\
                + "?dirList foaf:name ?name."\
                + "?dirList topMovies:KnownFor ?KnownFor."\
                + "?dirList topMovies:DTest ?DTest."\
                + "}"
    result = getGeneric(query, "Ontologies/directors.rdf")
    if result:
        for item in result:
            return item
    return None

def getCritique(movieName):
    query = "select ?IsCritiqueOf ?name ?Conveys ?TTest"\
                + "where { "\
                + "?rev topMovies:IsCritiqueOf '"+ movieName + "'."\
                + "?rev topMovies:IsCritiqueOf ?IsCritiqueOf."\
                + "?rev foaf:name ?name."\
                + "?rev topMovies:Conveys ?Conveys."\
                + "?rev topMovies:TTest ?TTest."\
                + "}"
    result = getGeneric(query, "Ontologies/nyTimes.rdf")
    if result:
        for item in result:
            return item
    return None

def getTweets(movieName):
    movieName = movieName.replace(" ","")
    movieName = "#"+movieName
    query = "select ?HasMovieTag ?name ?Tweets " \
            "?HasRetweetCount ?HasFollowers ?BelongsToCity " \
            "where {  " \
            "?tweetr topMovies:HasMovieTag '"+ movieName +"'. " \
            "?tweetr topMovies:HasMovieTag ?HasMovieTag. " \
            "?tweetr foaf:name ?name. " \
            "?tweetr topMovies:Tweets ?Tweets. " \
            "?tweetr topMovies:HasRetweetCount ?HasRetweetCount. " \
            "?tweetr topMovies:HasFollowers ?HasFollowers. " \
            "?tweetr topMovies:BelongsToCity ?BelongsToCity.}"
    result = getGeneric(query, "Ontologies/twitter.rdf")
    if result:
        if len(result) > 0:
            tweetString = ''
            for item in result:
                tweetString += "<tr><td>"+re.sub(r'[^\x00-\x7F]+',' ',item[2])+"</td></tr>"
            return tweetString
    return None

def getOmdb(movieName):
    query = "select ?HasTitle ?InYear ?HasActor ?HasDirector "\
                + "?FallsUnderGenre ?HasWonAwards ?HasRating ?HasRuntime"\
                + "?ReleaseDate ?Country ?Language ?HasPoster ?Test"\
                + "where { "\
                + "?movie topMovies:HasTitle '"+ movieName + "'."\
                + "?movie topMovies:HasTitle ?HasTitle."\
                + "?movie topMovies:InYear ?InYear."\
                + "?movie topMovies:HasActor ?HasActor."\
                + "?movie topMovies:HasDirector ?HasDirector."\
                + "?movie topMovies:FallsUnderGenre ?FallsUnderGenre."\
                + "?movie topMovies:HasWonAwards ?HasWonAwards."\
                + "?movie topMovies:HasRating ?HasRating."\
                + "?movie topMovies:HasRuntime ?HasRuntime."\
                + "?movie topMovies:ReleaseDate ?ReleaseDate."\
                + "?movie topMovies:BelongsToCountry ?Country."\
                + "?movie topMovies:Language ?Language."\
                + "?movie topMovies:HasPoster ?HasPoster."\
                + "?movie topMovies:Test ?Test."\
                + "}"
    result = getGeneric(query, "Ontologies/omdb.rdf")
    if result:
        for item in result:
            return item
    return None

def getAllMovies():
    query = 'PREFIX topMovies: <http://www.semanticweb.org/manohara/ontologies/2016/9/untitled-ontology-10#>\
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>\
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\
            PREFIX owl: <http://www.w3.org/2002/07/owl#>\
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>\
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>\
            select ?HasTitle ?HasPoster\
            where\
            {\
              ?movie topMovies:HasTitle ?HasTitle.\
              ?movie topMovies:HasPoster ?HasPoster.\
            }'
    result = getGeneric(query,"Ontologies/omdb.rdf")
    if len(result) > 0:
        returnString = ''
        for item in result:
            toReplaceString = "<img src='{{mimg}}' width='185' height='270'><br><a href='/search/?movieName={{mname}}'>{{mname}} </a><br><br>"
            toReplaceString = toReplaceString.replace("{{mimg}}",re.sub(r'[^\x00-\x7F]+',' ',item[1]))
            toReplaceString = toReplaceString.replace("{{mname}}",re.sub(r'[^\x00-\x7F]+',' ',item[0]))
            returnString += toReplaceString
        return returnString
    return None

# getAllMovies()
# movieName = "The Patriot"
# omdb = getOmdb(movieName)
# director = getDirectors(movieName)
# critique = getCritique(movieName)
# tweets = getTweets(movieName)



