import pymongo
import web
render=web.template.render("template")
class multipay:
    def GET(self):
        webinput=web.input()
        activity_id=webinput[u'activity_id']
        summoney=webinput[u'summoney']
        return render.multipay(summoney,activity_id)
class ShowPayPage:
    def GET(self):
        webinput=web.input()
        money=webinput[u'money']
        account=webinput[u'account']
        uid=webinput[u'uid']
        activity_id=webinput[u'activity_id']
        return render.simuAli(money,account,activity_id,uid) 

class multipayed:
    def POST(self):
        webinput=web.input()
        activity_id=webinput[u'activity_id']
        web.seeother("http://0.0.0.0:8080/refunded?activity_id="+activity_id)
class Pay:
    def POST(self):
        webinput=web.input()
        uid=webinput[u'uid']
        activity_id=webinput[u'activity_id']
        web.seeother("http://0.0.0.0:8080/payed?activity_id="+activity_id+"&uid="+uid)
        
