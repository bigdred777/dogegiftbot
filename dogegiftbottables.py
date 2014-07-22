

from sqlalchemy import Column, String,Float, Boolean
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import sessionmaker
import sqlalchemy as sql
import calendar
import datetime
def Timestamp(self,_datetime): 
        
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
class Posts(Base):
    post_id = Column(String, primary_key = True)
    __tablename__ = "posts"

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
    if search == None:
        search = Entries(user = User, entered = False)
    else:
        search.entered = False
    session.add(search)
    session.commit()
        
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
    all_winners = session.query(Contests).all()
    session.close()

    winners = []
    for item in all_winners:
        winners.append(item.winner)
    return winners    
def add_winner(Winner):
    db_add = Contests(winner = Winner,date = toTStamp(datetime.datetime.now()))
    session = create_session()
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
        line = read_file.readline().strip()
        add_entry(line)
        
