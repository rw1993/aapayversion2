import web
from urls import urls
import init_activities
render=web.template.render('template')
app=web.application(urls,globals())

if __name__=="__main__":
    init_activities.init_activities()
    app.run()
