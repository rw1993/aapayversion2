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
        return "hello"
