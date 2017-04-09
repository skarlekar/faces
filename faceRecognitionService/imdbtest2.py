import sys
from imdb import IMDb
i = IMDb()
#name = unicode('Mel Gibson', sys.getdefaultencoding(), 'replace')
name = "Mel Gibson"
results = i.search_person(name)
if len(results) > 0:
    person = results[0]
    i.update(person)
    #print person.summary()
    profile = {
        "name":name,
        "biography": person.summary().encode(sys.getdefaultencoding(), 'replace')
    }
    print profile
else:
    print "{} is not a celebrity".format(name)


#print person.summary().encode(sys.getdefaultencoding(), 'replace')
