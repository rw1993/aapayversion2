import pymongo
import web
render=web.template.render("template")
class ShowPayPage:
    def GET(self):
        webinput=web.input()
        money=webinput[u'money']
        account=webinput[u'account']
        uid=webinput[u'uid']
        activity_id=webinput[u'activity_id']
        print money
        return render.simuAli(money,account,activity_id,uid) 


class Pay:
    def POST(self):
        webinput=web.input()
        uid=webinput[u'uid']
        activity_id=webinput[u'activity_id']
        web.seeother("http://0.0.0.0:8080/payed?activity_id="+activity_id+"&uid="+uid)
        
