

from sqlalchemy import Column, String,Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sqlalchemy as sql
import calendar
import datetime
import uuid
def Timestamp(_datetime): 
        
    return calendar.timegm(_datetime.timetuple())

def toTStamp(DATETIME):
    """
    converts a datetime object into a date string
    """
    stamp = Timestamp(DATETIME)
    stamp = str(stamp)
    return stamp
def fromTStamp(stamp):
    """ Converts a date string into a datetime object"""
        
    date = datetime.datetime.utcfromtimestamp(float(stamp))
    return date
Base = declarative_base()

class Entries(Base):
    __tablename__ = "entries"
    user = Column(String, primary_key = True)
    times_won = Column(Float)
    entry_date = Column(String)
    entered = Column(Boolean)
    def __repr__(self):
        return "<entries instance %s >" % (self.user)
class Contests(Base):
    __tablename__ = "contest"
    date = Column(String, primary_key = True) #unix time
    winner = Column(String)
    prize = Column(String)
    prize_claimed = Column(Boolean)
    archived = Column(Boolean)
    
    def __cmp__(self,other):
        if type(self) == None or type(other) == "NoneType":
            return -1
        s = fromTStamp(self.date)
        o = fromTStamp(other.date)
        if s == o:
            return 0
        elif s > o:
            return -1
        else: 
            return 1
class Balance(Base):
    __tablename__ = "balance"
    balance_id =  Column(String, primary_key = True)
    balance = Column(Float)
    cost = Column(Float)
    needed = Column(Float)
    last_update = Column(String)
    
class Posts(Base):
    post_id = Column(String, primary_key = True)
    __tablename__ = "posts"
class Transactions(Base):
    __tablename__ = "transactions"
    tx_id = Column(String, primary_key = True)
    tx_type = Column(String)
    amount = Column(Float)
    donor = Column(String)
    date = Column(String)
    address = Column(String)
    def __repr__(self):
        return "<type: %s donor: %s amount: %.2f >" % (self.tx_type,self.donor,self.amount)

    def __cmp__(self, other):
        if type(self) == None or type(other) == None:
            return -1
        if self.date == other.date:
            return 0
        elif self.date > other.date:
            return -1
        else:
            return 1



def create_session():
    """
    Creates and returns a sqlite session
    """

    engine = sql.create_engine("sqlite:///dogegiftbot.db")
    Session = sessionmaker(bind=engine)
    session =Session()
    
    return session
def get_entries():

    session = create_session()
    all_entries = session.query(Entries).filter(Entries.entered == True).all()
    session.close()

    entries = []
    for item in all_entries:
        entries.append(item.user)
    return entries

def add_entry(User):
    session = create_session()
    
    search = session.query(Entries).filter(Entries.user==User).first()
    if search == None:
        db_add = Entries(user = User, entered = True)
        session = create_session()
        session.add(db_add)
        session.commit()
        print "added entry " + User
        return 1
    else:
        search.entered = True
        session.add(search)
        session.commit()
def find_entry(User):
    session = create_session()
    
    search = session.query(Entries).filter(Entries.user==User).first()
    if search == None:
        return None
    else:
        return search
        
def remove_entry(User):
    session = create_session()
    
    search = session.query(Entries).filter(Entries.user==User).first()
    print "remove ",
    print search 
    if search == None:
        return 0
    else:
        search.entered = False
        session.delete(search)
        session.commit()
    return 1
def count_entries():
    session = create_session()
    count = session.query(Entries).count()
    session.close()
    return str(count)
        
def get_posts():

    session = create_session()
    all_posts = session.query(Posts).all()
    session.close()

    posts = []
    for item in all_posts:
        posts.append(item.post_id)
    return posts
    
def add_post(Post):
    db_add = Posts(post_id = Post)
    session = create_session()
    session.add(db_add)
    session.commit()
    print "added post " + Post
    return 1
    
def convert_date(date):
    format = "%Y-%m-%d"
    datetime_ob = datetime.datetime.strptime(date,format)
    
    date_ob = datetime.date(int(datetime_ob.year),int(datetime_ob.month),int(datetime_ob.day))
    return date_ob
def get_winners():

    session = create_session()
    all_winners = session.query(Contests).filter(Contests.prize_claimed==False,Contests.archived==False).all()
    session.close()

    winners = []
    for item in all_winners:
        winners.append(item.winner)
    return winners    
def get_banned():
    
    session = create_session()
    all_winners = session.query(Contests).filter(Contests.prize_claimed==True,Contests.archived==False).all()
    session.close()

    winners = []
    for item in all_winners:
        winners.append(item.winner)
    return winners  
def new_contest(Winner):
    session = create_session()
        
    db_add = Contests(winner = Winner,date = toTStamp(datetime.datetime.utcnow()),prize = None,prize_claimed=False, archived = False)
    
    session.add(db_add)
    session.commit()
    print "added winner " + Winner
    
def add_winner(Winner,prize=None,claim=False,archived=False):
    session = create_session()
    search= session.query(Contests).filter(Contests.winner==Winner,Contests.archived==False).first()
    if search:
        if archived == True:

            search.archived = archived
        if prize !=None:
            search.prize = prize
        if claim == True:
            search.prize_claimed = True


        session.add(search)
        print " modified winner " + Winner
    else:
    
        db_add = Contests(winner = Winner,date = toTStamp(datetime.datetime.utcnow()),prize = prize,prize_claimed=claim, archived = archived)
    
        session.add(db_add)
        print "added winner " + Winner 
    session.commit()
    
    return 1

     

def remove_winner(Winner):
    session = create_session()
    
    db_remove = session.query(Contests).filter(Contests.winner==Winner,Contests.archived==False).first()
    print "removed " + db_remove.winner
    session.delete(db_remove)
    session.commit()
     
    
    
if __name__ == "__main__":

    
    engine = sql.create_engine("sqlite:///dogegiftbot.db")
   
    
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        session.execute("drop table balance")
    except:
        pass
    
    
    session.commit()
    
    session.close()
    
    Base.metadata.create_all(engine) 


    session = Session()
    session.commit()

    
def add_history_to_db(transactionsList,bot_name):
    bot_name= bot_name.lower()
    tips = {}
    d = {}
    w={}
    for tx in transactionsList:
        if tx["state"] != "completed":
            continue
        amount = float(tx["amount"].replace(",",""))
	from_user = tx["from_user"].lower()
	txType = tx["type"]
	txDate = tx["timestamp"][:10]
	to_user = tx["to_user"]


        if txType == "tip" and to_user == bot_name:
            name = txDate+ " " + from_user
            if name in tips:
                tips[name] += amount
            else:
                tips[name] = amount
        elif txType == "deposit":
            name =  txDate
            if name in d:
                d[name] += amount
            else:
                d[name] = amount
        elif txType == "withdraw":
           
            name =  txDate + " " +tx["to_address"]
            if name in w:
                w[name] += amount
            else:
                w[name] = amount


    session = create_session()
    
    for item in tips.keys():
        donor = item.split()[1]
        date = item.split()[0]
        search = session.query(Transactions).filter(Transactions.donor == donor,Transactions.date == date).first()
        if search:
            if search.amount < tips[item]:  
                search.amount = tips[item]
                session.add(search)
            
        else:
            session.add(Transactions(donor = donor,date = date, tx_id = str(uuid.uuid4()),tx_type = "tip",amount=tips[item]))

    for item in d.keys():
        donor = "anonymous deposit"
        date = item
        search = session.query(Transactions).filter(Transactions.donor == donor,Transactions.date == date).first()
        if search:
            if search.amount < d[item]:  
                search.amount = d[item]
                session.add(search)
            
        else:
            session.add(Transactions(donor = donor,date = date, tx_id = str(uuid.uuid4()),tx_type = "deposit",amount=d[item]))

    for item in w.keys():
        donor = "withdraw"
        date = item.split()[0]
        address = item.split()[1]
        search = session.query(Transactions)\
        .filter(Transactions.donor == donor,Transactions.date == date, Transactions.address==address).first()
        if search:
            if search.amount < w[item]:  
                search.amount = w[item]
                session.add(search)            
        else:
            session.add(Transactions(donor = donor,date = date, tx_id = str(uuid.uuid4()),tx_type = "withdraw",amount=w[item],address=address))

       
    
    session.commit()
    return
    
def get_todays_deposits():
    session = create_session()
    deposit = session.query(Transactions)\
    .filter(Transactions.date == str(datetime.date.today()),Transactions.tx_type == "deposit").first()
    session.close()
    if deposit:
        return deposit.amount
    else:
        return 0.0
def get_all_winners():
    
    session = create_session()
    all_winners = session.query(Contests).all()
    session.close()

    winners = []
    for item in all_winners:
        winners.append(item.winner)
    return winners    
def count_winners():
    session = create_session()
    count = session.query(Contests).count()
    session.close()
    return count
def timeout_winners():
    session = create_session()
    all_winners = session.query(Contests).filter(Contests.prize_claimed==False,Contests.archived==False).all()
    for winner in all_winners:
        date = fromTStamp(winner.date)
        if datetime.datetime.utcnow() - date > datetime.timedelta(days=3):
            print winner.winner,
            print " has timed out"
            session.delete(winner)
            session.commit()
            return winner.winner
            
    return None
    
def update_balance_db(balance,cost):
    session = create_session()
    search = session.query(Balance).filter(Balance.balance_id=="balance1").first()
    if search:
        search.balance= balance
        search.cost = cost
        search.needed = cost-balance
        search.last_update = toTStamp(datetime.datetime.utcnow())
    else:
        search = Balance(balance_id="balance1",balance = balance, cost=cost,
        needed = cost-balance,last_update = toTStamp(datetime.datetime.utcnow()))
    session.add(search)
    session.commit()