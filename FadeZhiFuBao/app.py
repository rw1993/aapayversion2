import web
from urls import urls
render=web.template.render("template")
app=web.application(urls,globals())

if __name__=="__main__":
    app.run()
