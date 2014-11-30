import pymongo
import web
from models.user import user
from models.activity import activity


render=web.template.render("template")
class show_current_activity:
    def GET(self):
        cookies=web.cookies()
        uid=cookies[u"uid"]
        u=user(uid=uid)
        current_host=[]
        for activity_id in u.hostlist:
            a=activity(activity_id=activity_id)
            if a.state=="wait_to_begin" or a.state=="wait_to_begin" or a.state=="pay_finished" or a.state=="start":
                current_host.append(a)
        current_in=[]
        for activity_id in u.inlist:
            a=activity(activity_id=activity_id)
            if a.state=="wait_to_begin" or a.state=="wait_to_begin" or a.state=="pay_finished" or a.state=="start":
                current_in.append(a)
        return render.activity_list(current_in,current_host,1)
        #return render.class_test(current_host,1)
class show_a_activity:
    def GET(self):
        cookies=web.cookies()
        webinput=web.input()
        myuid=cookies[u'uid']
        activity_id=webinput[u'activity_id']
        a=activity(activity_id=activity_id)
        p={}
        for people in a.people:
            if people[u'uid']==myuid:
                p=people
        t=0
        if myuid==a.host_uid:
            t=1
        else:
            t=2
        return render.activity_details(a,people,t)

        

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
        '''
        url="activity?activity_id="
        url+=str(activity_id)
        web.seeother(url)
        '''
        return "hello"
