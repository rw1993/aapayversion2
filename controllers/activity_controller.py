import pymongo
import web
from models.user import user
from models.activity import activity


render=web.template.render("template")
class begin_fill:
    def POST(self):
        cookies=web.cookies()
        uid=cookies[u'uid']
        u=user(uid=uid)
        webinput=web.input()
        activity_id=webinput[u'activity_id']
        a=activity(activity_id=int(activity_id))
        a.state="wait_to_fillmoney"
        string=u"\u6d3b\u52a8\u9700\u8981\u8865\u6b3e"
        for people in a.people:
            index=a.people.index(people)
            a.people[index][u'state']="unpay"
            uid=people[u'uid']
            money=webinput[str(uid)]
            a.people[index][u'money']=float(money)
            string+=" @"+people[u'screen_name']
        a.save()
        u.send_information(activity_id=int(activity_id),string=string)
        web.seeother("/activity?activity_id="+activity_id)
class set_fill_money:
    def GET(self):
        webinput=web.input()
        activity_id=webinput[u'activity_id']
        a=activity(activity_id=int(activity_id))
        return render.set_fill_money(a)
class end_activity:
    def POST(self):
        webinput=web.input()
        activity_id=webinput[u'activity_id']
        a=activity(activity_id=int(activity_id))
        a.state="end"
        a.save()
        web.seeother("/activity?activity_id="+activity_id)

        
class start_activity:
    def POST(self):
        cookies=web.cookies()
        uid=cookies[u'uid']
        u=user(uid=uid)
        webinput=web.input()
        activity_id=webinput[u'activity_id']
        a=activity(activity_id=int(activity_id))
        a.state="start"
        a.save()
        string=u"\u6d3b\u52a8\u5f00\u59cb"
        for people in a.people:
            string+=" @"+people[u'screen_name']
        u.send_information(activity_id=int(activity_id),string=string)
        web.seeother("/activity?activity_id="+activity_id)
class refunded:
    def GET(self):
        webinput=web.input()
        activity_id=webinput[u'activity_id']
        cookies=web.cookies()
        uid=cookies[u'uid']
        u=user(uid=uid)
        string=u"\u6211\u5df2\u7ecf\u9000\u6b3e\uff0c\u8bf7\u67e5\u6536"
        u.send_information(activity_id=int(activity_id),string=string)
        web.seeother("/activity?activity_id="+activity_id)
class set_refund_money:
    def POST(self):
        summoney=0.0
        webinput=web.input()
        activity_id=webinput[u'activity_id']
        a=activity(activity_id=int(activity_id))
        for people in a.people:
            money=webinput[str(people[u'uid'])]
            summoney+=float(money)
        url="http://0.0.0.0:8000/multipay?summoney="+str(summoney)+"&activity_id="+activity_id
        web.seeother(url)
class begin_refund:
    def GET(self):
        webinput=web.input()
        activity_id=webinput[u'activity_id']
        a=activity(activity_id=int(activity_id))
        return render.set_refund(a)
class refuse_activity:
    def POST(self):
        webinput=web.input()
        activity_id=webinput[u'activity_id']
        a=activity(activity_id=int(activity_id))
        a.state="refused"
        a.save()
        cookies=web.cookies()
        uid=cookies[u'uid']
        u=user(uid=uid)
        string=u'\u62b1\u6b49\uff0c\u6211\u65e0\u6cd5\u53c2\u52a0\u8fd9\u4e2a\u6d3b\u52a8'
        u.send_information(activity_id=int(activity_id),string=string)
        url="/activity?activity_id="+activity_id
        web.seeother(url)
class redesign_and_set:
    def POST(self):
        webinput=web.input()
        cookies=web.cookies()
        activity_id=webinput[u'activity_id']
        a=activity(activity_id=int(activity_id))
        a.activity_time=webinput[u'activity_time']
        a.activity_position=webinput[u'activity_position']
        a.activity_brief=webinput[u'activity_brief']
        uid=cookies[u'uid']
        people=[]
        u=user(uid=uid)
        for friend in u.get_friends_pachong():
            try:
                money=webinput[str(friend[u'id'])]
                p={}
                p[u'state']="invited"
                p[u'money']=float(money)
                p[u'uid']=friend[u'id']
                p[u'screen_name']=friend[u'screen_name']
                people.append(p)
            except:
                continue
        a.people=people
        a.save()
        string=u"\u6d3b\u52a8\u5df2\u7ecf\u91cd\u65b0\u8bbe\u8ba1"
        for p in people:
            string+=" @"+people[u'screen_name']
        u.send_information(activity_id=int(activity_id),string=string)
        url="activity?activity_id="+activity_id
        web.seeother(url)


class redesign_2_step:
    def POST(self):
        webinput=web.input()
        cookies=web.cookies()
        uid=cookies[u'uid']
        u=user(uid=uid)
        friends_invited=[]
        for friend in u.get_friends_pachong():
            try:
                uid=webinput[str(friend[u'id'])]
                friends_invited.append(friend)
            except:
                continue
        activity_id=webinput[u'activity_id']
        a=activity(activity_id=int(activity_id))
        return render.redesign_activity2(a,friends_invited)
                
class redesign_activity:
    def GET(self):
        webinput=web.input()
        activity_id=webinput[u'activity_id']
        a=activity(activity_id=int(activity_id))
        cookies=web.cookies()
        uid=cookies[u'uid']
        u=user(uid=uid)
        friends=u.get_friends_pachong()
        return render.redesign_activity1(a,friends)
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
            u=user(uid=uid)
            string=u"\u6211\u4ee5\u4ed8\u6b3e\uff0c\u8bf7\u67e5\u6536"
            u.send_information(activity_id=int(activity_id),string=string)
            ifchange=True
            for people in a.people:
                if people[u'state']=='payed':
                    ifchange=True
                else:
                    ifchange=False
                    break
            if ifchange:
                if a.state=="wait_to_pay":
                    a.state="pay_finished"
                else:
                    a.state="fillmoney_end"
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
        cookies=web.cookies()
        uid=cookies[u'uid']
        u=user(uid=uid)
        string=u"\u6d3b\u52a8\u5f00\u59cb\u6536\u6b3e\u4e86"
        for p in a.people:
            string+=" @"+p[u'screen_name']
        u.send_information(activity_id=int(activity_id),string=string)
        web.seeother("/activity?activity_id="+activity_id)

class attend_activity:
    def POST(self):
        webinput=web.input()
        activity_id=webinput[u'activity_id']
        cookies=web.cookies()
        uid=cookies[u'uid']
        u=user(uid=uid)
        u.attend_activity(int(activity_id))
        string=u"\u6211\u53c2\u52a0\u4e86\u6d3b\u52a8"
        u.send_information(activity_id=int(activity_id),string=string)
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
            if a.state=="end" or a.state=="wait_to_fill" or a.state=="fillmoney_end":
                past_host.append(a)
        past_in=[]
        for activity_id in u.inlist:
            a=activity(activity_id=activity_id)
            if a.state=="end" or a.state=="wait_to_fill" or a.state=="fillmoney_end":
                past_in.append(a)
        return render.activity_list(past_in,past_host,2)
class show_refused_activity:
    def GET(self):
        cookies=web.cookies()
        uid=cookies[u'uid']
        u=user(uid=uid)
        refuse_host=[]
        for activity_id in u.hostlist:
            a=activity(activity_id=activity_id)
            if a.state=="refused":
                refuse_host.append(a)
        refuse_in=[]
        for activity_id in u.inlist:
            a=activity(activity_id=activity_id)
            if a.state=="refused":
                refuse_in.append(a)
                print a.activity_id
        return render.activity_list(refuse_in,refuse_host,3)

        
class show_a_activity:
    def GET(self):
        cookies=web.cookies()
        webinput=web.input()
        myuid=cookies[u'uid']
        activity_id=webinput[u'activity_id']
        a=activity(activity_id=activity_id)
        p={}
        for people in a.people:
            if str(people[u'uid'])==myuid:
                p=people
        t=0
        if myuid==a.host_uid:
            t=1
        else:
            t=2
        return render.activity_details(a,p,t)

        

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
        
        ''' 
        for friend in invite_list:
            u=user(type=1,uid=int(friend['id']),name=friend['screen_name'])
            u.inlist.append(activity_id)
            u.save()
        '''
        url="activity?activity_id="
        url+=str(activity_id)
        web.seeother(url)
