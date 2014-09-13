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
    
class Donor():
    def __init__(self,donor,amount):
        self.amount = float(amount)
        self.donor = donor
    def __repr__(self):
        return "%s : %.2f" % (self.donor, self.amount)
    def __cmp__(self,other):
        return  other.amount-self.amount

        
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
            tx.dateobj = convert_date(tx.date)
            if "*" in tx.donor:
                continue
            total += tx.amount
            tips.append(tx)
        self.total = total
        self.tips = tips
        self.lastUpdate = datetime.datetime.now()
        donors = {}
        for tip in tips:
            if tip.donor in donors:
                donors[tip.donor] += tip.amount
            else:
                donors[tip.donor] = tip.amount
        donor_list =[]
        for key in donors.keys():
            donor_list.append(Donor(key,donors[key]))
        donor_list.sort()
        self.donors=donor_list
        
            


        
    def getTotal(self):
        
        if datetime.datetime.now() - self.lastUpdate > datetime.timedelta(minutes=5):
            self.update()  
        return self.total
    def getTips(self):
        if datetime.datetime.now() - self.lastUpdate > datetime.timedelta(minutes=5):
            self.update()
        return self.tips
    def returnTipWindow(self, numDays, start = datetime.date.today()):
        tipList = []
        for tip in self.tips:
            if start - tip.dateobj <= datetime.timedelta(days= numDays):
                tipList.append(tip)
        return tipList

class Winners(BaseDBObject):

    def update(self):
        session = create_session()
        self.winners = session.query(Contests).filter(Contests.prize_claimed==True,Contests.prize!=None).all()
        self.winners.sort()
        self.lastUpdate = datetime.datetime.now()
        session.close()
        self.pending = get_winners()
    def getWinners(self):
        if datetime.datetime.now() - self.lastUpdate > datetime.timedelta(minutes=5):
            self.update()
        return self.winners
    def getPending(self):
        return self.pending
class DogeTipBotBalance(BaseDBObject):
    def update(self):
        session = create_session()
        
        search = session.query(Balance).filter(Balance.balance_id == "balance1").first()
        if search:
            self.balance = search.balance
            self.cost = search.cost
            self.needed = search.needed
            self.last_history = search.last_update
        else:
            self.balance = 0
            self.cost = 0
            self.needed = 0
            self.last_history = datetime.datetime.utcnow()-datetime.timedelta(hours = 5)
        self.lastUpdate = datetime.datetime.now()
        session.close()
    def getBalance(self):
        if datetime.datetime.now() - self.lastUpdate > datetime.timedelta(minutes=1):
            self.update()
        return self.balance
        
    def getCost(self):
        if datetime.datetime.now() - self.lastUpdate > datetime.timedelta(minutes=1):
            self.update()
        return self.cost
    def printBalance(self):
        if datetime.datetime.now() - self.lastUpdate > datetime.timedelta(minutes=1):
            self.update()
        bal = float(self.getBalance())
        cost = float(self.getCost())
        while bal > cost:
            bal -= cost
        return bal

    



class BaseHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("static/index.html")
        
class StatusHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("static/status.html", balance = balance.printBalance(), cost = balance.getCost(), last_hist= fromTStamp(balance.last_history),\
        numWinners= count_winners(),numEntries = count_entries())
class HistoryHandler(tornado.web.RequestHandler):
    def get(self):
        try:
            window = int(self.get_argument("window"))
        except:
            window = 7
        self.render("static/history.html",total=tipHistory.getTotal(), tips = tipHistory.returnTipWindow(window),
        balance = balance.printBalance(), cost = balance.getCost(),window = window)
class WinnerHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("static/winners.html",winners = winners.getWinners(),datetime = datetime, fromTStamp = fromTStamp, pending = winners.getPending(),\
        winnerCount =count_winners())
class CheckHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("static/check.html",numEntries = count_entries())
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
        
class DonorHandler(tornado.web.RequestHandler):
    def get(self):

        self.render("static/donors.html",donors = tipHistory.donors)
    

       


                


STATIC_PATH= os.path.join(os.path.dirname(__file__),r"static/")
application = tornado.web.Application([
	(r"/", StatusHandler),
	(r"/about", BaseHandler),
	(r"/history",HistoryHandler),
	(r"/winners",WinnerHandler),
	(r"/check",CheckHandler),
	(r"/status",StatusHandler),
	(r"/checkapi",CheckAPI),
        (r"/donors",DonorHandler),
],static_path=STATIC_PATH,login_url=r"/login/", #debug=True,
 cookie_secret="35wfa35tgtres5wf5tyhxbt4"+str(random.randint(0,1000000)))

if __name__ == "__main__":
    tipHistory = TipHistory()
    winners = Winners()
    balance = DogeTipBotBalance()
    


    
    application.listen(80)
    tornado.ioloop.IOLoop.instance().start()
    




