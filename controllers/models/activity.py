import pymongo

class activity:
    def init(self,activity_id):
        activities=self.get_activities()
        a=activities.find_one({u'activity_id':int(activity_id)})
        self.activity_id=a[u'activity_id']
        self.activity_name=a[u'activity_name']
        self.activity_time=a[u'activity_time']
        self.activity_brief=a[u'activity_brief']
        self.activity_money=a[u'activity_money']
        self.activity_position=a[u'activity_position']
        self.state=a[u'state']
        self.people=a[u'people']
        self.host_uid=a[u'host_uid']
        self.host_name=a[u'host_name']
        print self.activity_id
    def set_activity_id(self):
        activities=self.get_activities()
        counter=activities.find_one({u'type':"counter"})
        self.activity_id=counter[u'count']+1
        activities.update({u'type':"counter"},{"$set":{u'count':self.activity_id}})


    def get_activities(self):
        con=pymongo.Connection("localhost",27017)
        aap2=con.aap2
        activities=aap2.activities
        return activities


    def send_invite_weibo(self,client):
        text=u"I invite you all to a activity!To see the details,please click http://0.0.0.0:8080?from_activity_id="+str(self.activity_id)+"  "
        for people in self.people:
            text+="@"+people[u'screen_name']+" "
        client.statuses.update.post(status=text)


    def save(self):
        activities=self.get_activities()
        activities.remove({"activity_id":self.activity_id})
        a={}
        a[u'activity_id']=self.activity_id
        a[u'activity_name']=self.activity_name
        a[u'activity_time']=self.activity_time
        a[u'activity_brief']=self.activity_brief
        a[u'activity_money']=self.activity_money
        a[u'activity_position']=self.activity_position
        a[u'people']=self.people
        a[u'state']=self.state
        a[u'host_name']=self.host_name
        a[u'host_uid']=self.host_uid
        activities.insert(a)


    def __init__(self,activity_name=None,activity_money=None,activity_time=None,activity_position=None,activity_brief=None,friends_in=None,host_uid=None,hostinfor=None,client=None,activity_id=None):
        
        if not(activity_id is None):
            self.init(activity_id)
        else:
            self.activity_name=activity_name
            self.activity_money=activity_money
            self.activity_time=activity_time
            self.activity_position=activity_position
            self.activity_brief=activity_brief
            self.host_uid=host_uid
            self.host_name=hostinfor[u'screen_name']
            self.state="wait_to_begin"
            self.people=[]
            money=float(self.activity_money)/(len(friends_in)+1)
            for friend in friends_in:
                p={}
                p[u'state']="invited"
                p[u'uid']=int(friend['id'])
                p['screen_name']=friend['screen_name']
                p[u'money']=money
                self.people.append(p)
            self.set_activity_id()
            self.send_invite_weibo(client)
            self.save()
        
            

