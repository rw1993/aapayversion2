import weibo
import pymongo
import web


class user:
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
        aapay2=con.aapay2
        users=aapay2.users
        return users
    def InitWithUid(self,uid):
        users=self.getusers()
        u=users.find_one({u'uid':uid})
        self.uid=uid
        if u is None:
            cookies=web.cookies()
            self.access_token=cookies[u'access_token']
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

    def getclient(self,access_token,expires_in):
        appkey='3541987275'
        appsecret='9e2cca6d2f735a7ebee4999ac6608231'
        redirecturl='http://0.0.0.0:8080/redirecturl'
        client=weibo.APIClient(app_key=appkey,app_secret=appsecret,redirect_uri=redirecturl)
        client.set_access_token(access_token,expires_in)
        return client



    def InitWithCode(self,code):
        appkey='3541987275'
        appsecret='9e2cca6d2f735a7ebee4999ac6608231'
        redirecturl='http://0.0.0.0:8080/redirecturl'
        client=weibo.APIClient(app_key=appkey,app_secret=appsecret,redirect_uri=redirecturl)
        result=client.request_access_token(str(code))
        self.access_token=result[u'access_token']
        self.expires_in=result[u'expires_in']
        client.set_access_token(self.access_token,self.expires_in)
        web.setcookie(u'access_token',self.access_token)
        web.setcookie(u'expires_in',self.access_token)
        self.uid=result[u'uid']
        web.setcookie(u'uid',self.uid)
        self.InitWithUid(self.uid)
    

    def __init__(self,uid=None,code=None):
        if uid is None:
            self.InitWithCode(code)
        else:
            self.InitWithUid(uid)
    



    def get_user_info_weibo(self):
        client=self.getclient(self.access_token,self.expires_in)
        userinfor=client.users.show.get(uid=int(self.uid))
        return userinfor

