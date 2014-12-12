import weibo
import pymongo
import web
import GetWeiBo
from activity import activity
class user:
    def attend_activity(self,activity_id):
        a=activity(activity_id=activity_id)
        self.inlist.append(activity_id)
        index=-1
        for people in a.people:
            if int(people[u'uid'])==int(self.uid):
                index=a.people.index(people)
                print a.people[index][u'screen_name']
                break
        a.people[index][u'state']='in'
        ifchange=True
        for people in a.people:
            if people['state']=="in":
                ifchange=True
            else:
                ifchange=False
                break
        if ifchange:
            a.state="people_all_in"
        a.save()
        self.save()
    def set_a_activity(self,activity_name,activity_money,activity_time,activity_position,activity_brief,friends_in):
        self.get_from_cookie()
        client=self.getclient(self.access_token,self.expires_in)
        hostinfor=self.get_user_info_weibo()
        newactivity=activity(activity_name,activity_money,activity_time,activity_position,activity_brief,friends_in,self.uid,hostinfor,client)
        self.hostlist.append(newactivity.activity_id)
        self.save()
        return newactivity.activity_id


    def get_friends_pachong(self):
        p=GetWeiBo.pachong()
        client=p.getClient()
        self.get_from_cookie()
        result=client.friendships.friends.bilateral.get(uid=int(self.uid),count=200)
        friends=result[u'users']
        return friends
        

    def save(self):
        users=self.getusers()
        users.remove({u'uid':self.uid})
        u={}
        u['name']=self.name
        u['uid']=self.uid
        u['account']=self.account
        u['hostlist']=self.hostlist
        u['inlist']=self.inlist
        u['informations']=self.informations
        users.insert(u)

    def getusers(self):
        con=pymongo.Connection("localhost",27017)
        aap2=con.aap2
        users=aap2.users
        return users

    def InitWithUid(self,uid):
        users=self.getusers()
        u=users.find_one({u'uid':str(uid)})
        self.uid=str(uid)
        if u is None:
            print "not in"
            self.hostlist=[]
            self.inlist=[]
            self.informations=[]
            client=self.getclient(self.access_token,self.expires_in)
            userinfor=client.users.show.get(uid=int(self.uid))
            self.name=userinfor[u'name']
            self.account=""
            self.save()
        else:
            self.hostlist=u['hostlist']
            self.inlist=u['inlist']
            self.name=u['name']
            self.informations=u[u'informations']
            self.account=u[u'account']

    def getclient(self,access_token,expires_in):
        appkey='3541987275'
        appsecret='9e2cca6d2f735a7ebee4999ac6608231'
        redirecturl='http://0.0.0.0:8080/redirecturl'
        client=weibo.APIClient(app_key=appkey,app_secret=appsecret,redirect_uri=redirecturl)
        client.set_access_token(access_token,expires_in)
        return client
    def send_information(self,activity_id,string):
        self.get_from_cookie()
        client=self.getclient(self.access_token,self.expires_in)
        result=client.comments.create.post(id=int(activity_id),comment=string)
        print result



    def InitWithCode(self,code):
        appkey='3541987275'
        appsecret='9e2cca6d2f735a7ebee4999ac6608231'
        redirecturl='http://0.0.0.0:8080/redirecturl'
        client=weibo.APIClient(app_key=appkey,app_secret=appsecret,redirect_uri=redirecturl)
        result=client.request_access_token(str(code))
        self.access_token=result[u'access_token']
        self.expires_in=result[u'expires_in']
        client.set_access_token(self.access_token,self.expires_in)
        web.setcookie('access_token',self.access_token)
        web.setcookie('expires_in',self.expires_in)
        self.uid=str(result['uid'])
        web.setcookie(u'uid',str(self.uid))
        self.InitWithUid(self.uid)
    def InitWithOthersUid(self,uid,name):
        users=self.getusers()
        u=users.find_one({'uid':uid})
        if u is None:
            self.account=''
            self.name=name
            self.uid=uid
            self.inlist=[]
            self.hostlist=[]
            self.informations=[]
            self.save()
        else:
            self.InitWithUid(uid)

    def __init__(self,type=0,uid=None,code=None,name=None):
        if type==1:
            self.InitWithOthersUid(uid,name)
        elif uid is None:
            self.InitWithCode(code)
        else:
            self.InitWithUid(str(uid))
    

    def set_account(self,account):
        self.account=account
        self.save()


    def get_from_cookie(self):
        cookies=web.cookies()
        #print cookies['uid']
        #print cookies['access_token']
        #print cookies['expires_in']
        self.uid=cookies['uid']
        self.access_token=cookies['access_token']
        self.expires_in=cookies['expires_in']
    def get_user_info_weibo(self):
        try:
            self.get_from_cookie()
        except:
            print "access_token unset"
        client=self.getclient(access_token=self.access_token,expires_in=self.expires_in)
        userinfor=client.users.show.get(uid=int(self.uid))
        return userinfor

