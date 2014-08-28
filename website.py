# -*- coding: utf-8 -*-
import tornado.ioloop
import tornado.web
import tornado
import os
import datetime
import random
from dogegiftbottables import *
from sqlalchemy import or_
class BaseDBObject():
    def __init__(self):
       self.update()
    
class TipHistory(BaseDBObject):

    def update(self):
        
        session = create_session()
        txs = session.query(Transactions)\
        .filter(or_(Transactions.tx_type =="tip",Transactions.tx_type =="deposit")).all()
        session.close()
        txs.sort()
        tips = []
        total = 0
        for tx in txs:
            if "*" in tx.donor:
                continue
            total += tx.amount
            tips.append(tx)
        self.total = total
        self.tips = tips
        self.lastUpdate = datetime.datetime.now()
        
    def getTotal(self):
        
        if datetime.datetime.now() - self.lastUpdate > datetime.timedelta(minutes=1):
            print "update"
            self.update()  
        return self.total
    def getTips(self):
        if datetime.datetime.now() - self.lastUpdate > datetime.timedelta(minutes=5):
            self.update()
        return self.tips

class Winners(BaseDBObject):

    def update(self):
        session = create_session()
        self.winners = session.query(Contests).filter(Contests.prize_claimed==True,Contests.prize!=None).all()
        self.winners.sort()
        self.lastUpdate = datetime.datetime.now()
        session.close()
    def getWinners(self):
        if datetime.datetime.now() - self.lastUpdate > datetime.timedelta(minutes=30):
            self.update()
        return self.winners
class DogeTipBotBalance(BaseDBObject):
    def update(self):
        session = create_session()
        search = session.query(Balance).filter(Balance.balance_id == "balance1").first()
        self.balance = search.balance
        self.cost = search.cost
        self.needed = search.needed
        self.lastUpdate = datetime.datetime.now()
        session.close()
    def getBalance(self):
        if datetime.datetime.now() - self.lastUpdate > datetime.timedelta(minutes=5):
            self.update()
        return self.balance
        
    def getCost(self):
        if datetime.datetime.now() - self.lastUpdate > datetime.timedelta(minutes=5):
            self.update()
        return self.cost

    



class BaseHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("static/index.html")
class HistoryHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("static/history.html",total=tipHistory.getTotal(), tips = tipHistory.getTips(),
        balance = balance.getBalance(), cost = balance.getCost() )
class WinnerHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("static/winners.html",winners = winners.getWinners(),datetime = datetime, fromTStamp = fromTStamp)
class CheckHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("static/check.html")
class CheckAPI(tornado.web.RequestHandler):
    def get(self):
        try:
            user = self.get_argument("user")
        except:
            self.write("False")
            return 
        if find_entry(user):
            self.write("True")
        else:
            self.write("False")
        
    
    

       


                


STATIC_PATH= os.path.join(os.path.dirname(__file__),r"static/")
application = tornado.web.Application([
	(r"/", BaseHandler),
	(r"/history",HistoryHandler),
	(r"/winners",WinnerHandler),
	(r"/check",CheckHandler),
	(r"/checkapi",CheckAPI),

],static_path=STATIC_PATH,login_url=r"/login/", #debug=True,
 cookie_secret="35wfa35tgtres5wf5tyhxbt4"+str(random.randint(0,1000000)))

if __name__ == "__main__":
    tipHistory = TipHistory()
    winners = Winners()
    balance = DogeTipBotBalance()
    


    
    application.listen(80)
    tornado.ioloop.IOLoop.instance().start()
    




