import web
from models.user import user
render=web.template.render("template")
class forau:
    def GET(self):
        webinput=web.input()
        try:
            weibo_id=webinput[u'from_activity_id']
            web.setcookie('from_activity_id',weibo_id)
            return render.index()
        except:
            return render.index()
class redirect_uri:
    def GET(self):
        webinput=web.input()
        code=webinput[u'code']
        u=user(code=code)
        if u.account=="":
            web.seeother("/set_account_page")
        else:
            try:
                cookies=web.cookies()
                weibo_id=cookies[u'from_activity_id']
                #print weibo_id
                web.seeother("activity?activity_id="+weibo_id)
            except:
                userinfor=u.get_user_info_weibo()
                informations=u.informations
                return render.user_index(userinfor,informations,u.account)





class show_design_activity_page:
    def GET(self):
        cookies=web.cookies()
        uid=cookies[u'uid']
        u=user(uid=uid)
        friends=u.get_friends_pachong()
        return render.design_activity(friends)

class show_user_index():
    def GET(self):
        cookies=web.cookies()
        uid=cookies[u'uid']
        u=user(uid=uid)
        informations=u.informations
        userinfor=u.get_user_info_weibo()
        return render.user_index(userinfor,informations,u.account)


class show_set_account_page:
    def GET(self):
        return render.set_account_page()

class set_account:
    def POST(self):
        webinput=web.input()
        cookies=web.cookies()
        account=webinput[u'account']
        uid=cookies[u'uid']
        u=user(uid=uid)
        u.set_account(account)
        userinfor=u.get_user_info_weibo()
        informations=u.informations
        try:
            activity_id=cookies[u'from_activity_id']
            web.seeother("/activity?activity_id="+activity_id)
        except:
            return render.user_index(userinfor,informations,u.account)
