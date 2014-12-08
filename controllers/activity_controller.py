import pymongo
import web
from models.user import user
from models.activity import activity


render=web.template.render("template")
class redesign_activity:
    def GET(self):
        webinput=web.input()
        activity_id=webinput[u'activity_id']
        a=activity(activity_id=int(activity_id))
        cookies=web.cookies()
        uid=cookies[u'uid']
        u=user(uid=uid)
        friends=u.get_friends_pachong()
        return render.redesign_activity(a,friends)
class payed:
    def GET(self):
        webinput=web.input()
        uid=webinput[u'uid']
        activity_id=webinput[u'activity_id']
        a=activity(activity_id=int(activity_id))
        index=-1
        for people in a.people:
            if str(people[u'uid'])==str(uid):
                index=a.people.index(people)
                break
        if index>=0:
            a.people[index][u'state']='payed'
            ifchange=True
            for people in a.people:
                if people[u'state']=='payed':
                    ifchange=True
                else:
                    ifchange=False
                    break
            if ifchange:
                a.state="pay_finished"
            a.save()
            web.seeother("/activity?activity_id="+activity_id)
        else:
            return "error"
class pay:
    def POST(self):
        webinput=web.input()
        cookies=web.cookies()
        activity_id=webinput[u'activity_id']
        a=activity(activity_id=int(activity_id))
        host=user(uid=a.host_uid)
        account=host.account
        myuid=cookies[u'uid']
        money=-1
        for people in a.people:
            if str(people[u'uid'])==str(myuid):
                money=people[u'money']
                break
        if money>0:
            web.seeother("http://0.0.0.0:8000/raisepay?account="+account+"&money="+str(money)+"&activity_id="+activity_id+"&uid="+str(myuid))
        else:
            return "error"

class begin_to_pay:
    def POST(self):
        webinput=web.input()
        activity_id=webinput[u'activity_id']
        cookies=web.cookies()
        a=activity(activity_id=int(activity_id))
        a.state="wait_to_pay"
        a.save()
        web.seeother("/activity?activity_id="+activity_id)

class attend_activity:
    def POST(self):
        webinput=web.input()
        activity_id=webinput[u'activity_id']
        cookies=web.cookies()
        uid=cookies[u'uid']
        u=user(uid=uid)
        u.attend_activity(int(activity_id))
        web.seeother("/activity?activity_id="+activity_id)
class show_current_activity:
    def GET(self):
        cookies=web.cookies()
        uid=cookies[u"uid"]
        u=user(uid=uid)
        current_host=[]
        for activity_id in u.hostlist:
            a=activity(activity_id=activity_id)
            if a.state=="wait_to_begin" or a.state=="wait_to_pay" or a.state=="pay_finished" or a.state=="start" or a.state=='people_all_in':
                current_host.append(a)
        current_in=[]
        for activity_id in u.inlist:
            a=activity(activity_id=activity_id)
            if a.state=='wait_to_pay' or a.state=="wait_to_begin" or a.state=="people_all_in" or a.state=="pay_finished" or a.state=="start":
                current_in.append(a)
        return render.activity_list(current_in,current_host,1)
class show_past_activity:
    def GET(self):
        cookies=web.cookies()
        uid=cookies[u'uid']
        u=user(uid=uid)
        past_host=[]
        for activity_id in u.hostlist:
            a=activity(activity_id=activity_id)
            if a.state=="end" or a.state=="wait_to_fill":
                past_host.append(a)
        past_in=[]
        for activity_id in u.inlist:
            a=activity(activity_id=activity_id)
            if a.state=="end" or a.state=="wait_to_fill":
                past_in.append(a)
        return render.activity_list(past_host,past_in,2)
        
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
        url="activity?activity_id="
        url+=str(activity_id)
        web.seeother(url)
