

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
    date = Column(String, primary_key = True)
    winner = Column(String)
    prize = Column(String)
    prize_claimed = Column(Boolean)
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
        print "added " + User
        return 1
    else:
        search.entered = True
        session.add(search)
        session.commit()
    
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
        
def get_posts():

    session = create_session()
    all_posts = session.query(Posts).all()
    session.close()

    posts = []
    for item in all_posts:
        posts.append(item.user)
    return posts
    
def add_post(Post):
    db_add = Posts(post_id = Post)
    session = create_session()
    session.add(db_add)
    session.commit()
    print "added post " + Post
    return 1
    

def get_winners():

    session = create_session()
    all_winners = session.query(Contests).filter(Contests.prize_claimed==False).all()
    session.close()

    winners = []
    for item in all_winners:
        winners.append(item.winner)
    return winners    
def get_banned():
    
    session = create_session()
    all_winners = session.query(Contests).filter(Contests.prize_claimed==True).all()
    session.close()

    winners = []
    for item in all_winners:
        winners.append(item.winner)
    return winners  
    
def add_winner(Winner,prize=None,claim=False):
    session = create_session()
    search = session.query(Contests).filter(Contests.winner==Winner).first()
    if search != None:
        search.prize = prize 
        search.prize_claimed = claim
        session.add(search)
    else:
    
        db_add = Contests(winner = Winner,date = toTStamp(datetime.datetime.now()),prize = prize,prize_claimed=claim)
    
        session.add(db_add)
    session.commit()
    print "added winner " + Winner 
    return 1

def remove_winner(Winner):
    session = create_session()
    
    db_remove = session.query(Contests.winner == Winner).first()
    
    session.delete(db_remove)
    session.commit()
     
    
    
if __name__ == "__main__":

    
    engine = sql.create_engine("sqlite:///dogegiftbot.db")
    Base.metadata.create_all(engine) 

    Session = sessionmaker(bind=engine)
    session = Session()
    session.commit()
    with open("entries.txt") as  read_file:
        for line in read_file:
            if line.strip == "":
                break
            add_entry(line.strip())
        
def add_history_to_db(tip_bot_text,bot_name):
    text = tip_bot_text.replace('|',' ').encode("ascii","replace")
    text2 = text.split("\n")
    text3 = []
    tips = {}
    d = {}
    w={}
    for line in text2:
        if bot_name in line:
            text3.append(line.split())
    for tx in text3:
        if tx[1] == "failed":
            continue
        if tx[0] == "tip":
            name = tx[2]+ " " + tx[4]
            if name in tips:
                tips[name] += float(tx[6])
            else:
                tips[name] = float(tx[6])
        elif tx[0] == "d":
            name =  tx[4]
            if name in d:
                d[name] += float(tx[6])
            else:
                d[name] = float(tx[6])
        elif tx[0] == "w":
           
            name =  tx[4] + " " +tx[5]
            if name in w:
                w[name] += float(tx[6])
            else:
                w[name] = float(tx[6])

    session = create_session()
    
    for item in tips.keys():
        donor = item.split()[0]
        date = item.split()[1]
        search = session.query(Transactions).filter(Transactions.donor == donor,Transactions.date == date).first()
        if search == None:
            session.add(Transactions(donor = donor,date = date, tx_id = str(uuid.uuid4()),tx_type = "tip",amount=tips[item]))
        else:
            if search.amount < tips[item]:  
                search.amount = tips[item]
                session.add(search)
    for item in d.keys():
        donor = "anonymous deposit"
        date = item
        search = session.query(Transactions).filter(Transactions.donor == donor,Transactions.date == date).first()
        if search == None:
            session.add(Transactions(donor = donor,date = date, tx_id = str(uuid.uuid4()),tx_type = "deposit",amount=d[item]))
        else:
            if search.amount < d[item]:  
                search.amount = d[item]
                session.add(search)
    for item in w.keys():
        donor = "withdraw"
        date = item.split()[0]
        address = item.split()[1]
        search = session.query(Transactions)\
        .filter(Transactions.donor == donor,Transactions.date == date, Transactions.address==address).first()
        if search == None:
            session.add(Transactions(donor = donor,date = date, tx_id = str(uuid.uuid4()),tx_type = "withdraw",amount=w[item],address=address))
        else:
            if search.amount < w[item]:  
                search.amount = w[item]
                session.add(search)
        
    
    session.commit()
    return
    

        
    