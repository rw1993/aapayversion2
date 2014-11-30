import pymongo

def init_activities():
    con=pymongo.Connection("localhost",27017)
    aap2=con.aap2
    activities=aap2.activities
    counter=activities.find_one({u'type':"counter"})
    if counter is None:
        counter={}
        counter[u'type']="counter"
        counter[u'count']=0
        activities.insert(counter)
