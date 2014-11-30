import pymongo
import web
from models.user import user
from models.activity import activity


render=web.template.render("template")

class show_a_activity:
    def GET(self):
        cookies=web.cookies()
        webinput=web.input()
        myuid=cookies[u'uid']
        activity_id=webinput[u'activity_id']
        a=activity(activity_id=activity_id)
        return render.test(a)

        

class set_a_activity:
    def POST(self):
        cookies=web.cookies()
        webinput=web.input()
        uid=cookies[u'uid']
        hostuser=user(uid=uid)
        friends=hostuser.get_friends_pachong()
        invite_list=[]
        for friend in friends:
            try:
                test=webinput[str(friend[u'id'])]
                invite_list.append(friend)
            except:
                continue
        activity_id=hostuser.set_a_activity(activity_name=webinput[u'ActivityName'],activity_money=webinput[u'ActivityMoney'],activity_time=webinput[u'ActivityTime'],activity_position=webinput[u'ActivityPosition'],activity_brief=webinput[u'ActivityBrief'],friends_in=invite_list)
        
        
        for friend in invite_list:
            u=user(type=1,uid=friend['id'],name=friend['screen_name'])
            u.inlist.append(activity_id)
            u.save()
    
        url="activity?activity_id="
        url+=str(activity_id)
        web.seeother(url)

