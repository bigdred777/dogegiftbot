import praw
r = praw.Reddit(user_agent='dogegiftbot version 0.1')
winner_count = 0
r.login()
r.send_message('dogetipbot','hist','+history')

msgs = r.get_unread()


