from weibo import APIClient



class pachong:
    def __init__(self):
	Appkey="3423280349"
        Appsecret="1f74f37b71c5ca2e0faadc41129d516a"
        callbackurl="http://www.baidu.com"
        ack="2.00pVrsKC3mz1gE840b5f298788d81D"
        expin="7801776"
        self.client=APIClient(app_key=Appkey,app_secret=Appsecret)
        self.client.set_access_token(ack,expin)

    def getClient(self):
        return self.client
