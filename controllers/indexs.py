import web
from models.user import user
render=web.template.render("template")
class forau:
    def GET(self):
        webinput=web.input()
        try:
            weibo_id=webinput[u'from_weibo_id']
            web.setcookie('from_weibo_id',weibo_id)
            return render.index()
        except:
            return render.index()
class redirect_uri:
    def GET(self):
        webinput=web.input()
        code=webinput[u'code']
        u=user(code=code)
        if u.account=="":
            web.seeother("set_accout_page")
        else:
            try:
                cookies=web.cookies()
                weibo_id=cookies[u'from_weibo_id']
                print weibo_id
                web.seeother("activity?weibo_id="+weibo_id)
            except:
                userinfor=user.get_user_info_weibo()
                informations=user.informations
                return render.userindex(userinfor,informations)

class show_set_accout_page:
    def GET(self):
        return render.set_account_page()
