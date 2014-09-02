import praw
import time
import random
import sys
import urllib
import urllib2
import json
import StringIO
import traceback
from dogegiftbottables import *
import hashlib
from dogegiftbotmessages import dogegiftbotmessages
import requests
m = dogegiftbotmessages()
r = praw.Reddit(user_agent='dogegiftbot version 1.1')

###### config section ############
bot_name = "dogemultisigescrow"
#authorized admins
authorized = ['Doomhammer458']
#login info
r.login()                  #leave blank for praw config
reentry_contact = "Doomhammer458"
subreddit_to_post = "dogetrivia"
freq_bal_check = 10 # time in minute
contest_freq = 5 

###### config section ############


# Created by /u/PieMan2201 through bots4doge.com
    


bot_name = bot_name.lower()
winner_count = 0

print 'LOGIN SUCCESS'
kill_var = '321'
winners = []
msgcheck = 0
history_hash = None
balance = 0

entries = get_entries()
#r.send_message('dogetipbot','hist','+history')

last_bal_check = datetime.datetime.now() - datetime.timedelta(days=5)
last_con_check = datetime.datetime.now() - datetime.timedelta(days=5)
last_his_succ =  datetime.datetime.now() - datetime.timedelta(days=5)
done = get_posts()
donors = []
donations = []
donor_dict = {}



already_won = get_winners()


print entries
print already_won
print done
def getDonors(text):
        
	text2 = text.replace('|',' ').encode("ascii","replace")
	dict = {}
	text3 = StringIO.StringIO(text2)
	counter = 0
        anon_count = 0
	for line in text3:
	        
	        if "**/u/"+bot_name+"**" in line:
	           
	            
	            if line.split()[0] == "tip":
	                  
	                

		    
		         if line.split()[3] == '**/u/'+bot_name+'**' and line.split()[1] == "?" and counter <10:
		         	        

		         	        
		        	if line.split()[2] not in dict.keys():
		        		        
		           	  dict[line.split()[2]] = float(line.split()[7])
		           	  counter += 1
		        	elif line.split()[2] in dict.keys():
                                    dict[line.split()[2]] = dict[line.split()[2]] + float(line.split()[7])
                                    
                    elif line.split()[0] == "d":
                        anon_count+=1
                        dict["anonymous "+str(anon_count)] = float(line.split()[7])
                        counter+=1
                        
                if counter == 10:
                    break
                    
	print "donors "	   
	print dict                              
        return dict	
def getaddress(winner,card):
	url = 'http://ws-egifter.egifter.com/API/v1/DogeAPI.aspx'
	form = {
		'user_id':winner,
		'card_name':card,
		'card_amount':25.0
	}
	json1 = json.dumps(form)
	request = urllib2.Request(url, json1)
	f = urllib2.urlopen(request)
	address = f.read()[54:-17]
	return address
def savelists(entries, already_won, done):
	file = open('entries.txt','w')
	list = []
	for x in entries:
		mooting = str(x)
#		print mooting
		list.append(mooting)
	for x in list:
		file.write('%s \n' % x)
	file2 = open('winners.txt','w')
	list = []
	for x in already_won:
		mooting = str(x)
#		print mooting
		list.append(mooting)
	for x in list:
		file2.write('%s \n' % x)
	file3 = open('postids.txt','w')
	list = []
	for x in done:
		mooting = str(x)
#		print mooting
		list.append(mooting)
	for x in list:
		file3.write('%s \n' % x)
	file.close()
	file2.close()
	file3.close()
def getcost():
	status_code = 404
	while status_code != 200:
           	f = requests.get('https://x.g0cn.com/prices')
           	status_code = f.status_code
           	price_dict = f.json()
           	xdg_price = float(price_dict["prices"]["XDG"]["USD"])**-1
           	cost = xdg_price * 26
           	cost_two = cost + 100
        if cost_two < 100000:
            return 1000000000.0
        return cost_two
           	
def check_commands():
	print 'Checking messages'
	msgs = r.get_unread(limit=None)
	for msg in msgs:
	        global balance
	        if type(msg) != praw.objects.Message:
	            msg.mark_as_read()
	            print "NEW comment reply: ",
	            print msg
	            continue
	        
	        entries = get_entries()
	        already_won=get_winners()
	        banned=get_banned()
		body = msg.body.lower()
		auth = msg.author.name
		if auth== "dogetipbot":
		    print "DOGETIPBOT message"
		    if 'here are your last' in body:
                        get_dtbinfo(body)
                        msg.mark_as_read()
                        global last_his_succ
                        last_his_succ = datetime.datetime.now()
                        update_balance_db(float(balance),float(getcost()))
                        
		    else:
		        msg.mark_as_read()
		       
		        print body.replace('|',' ').encode("ascii","replace")
		        print
		        continue

		
		elif '+ent' in body:
			print "Processing ENTRY request"
			msg.mark_as_read()
			user = r.get_redditor(auth)
			comkarm = user.comment_karma
			linkkarm = user.link_karma
			if int(comkarm) > 49 or int(linkkarm) > 49:
				if auth not in entries and auth not in already_won and auth not in banned:
					add_entry(auth)
					msg.reply('You have been entered into the giveaway! '+m.footer)
					print auth + ' has entered'
				else:
					msg.reply('Silly shibe! You can only enter once.'+m.footer)
					print auth + ' is a silly shibe'
			else:
				print auth + ' does not meet requirements'
				msg.reply("I'm sorry, but you do not have sufficient comment / link karma  to register. You need at least 50 comment / link karma to enter."+m.footer)

			
			print 'Request processed'
			
		elif '+opt'in body and auth in entries:
			print 'Processing OPT-OUT request'
			msg.mark_as_read()
			remove_entry(auth)
			msg.reply('You have been removed from the giveaway. '+m.footer)
			
			print 'Request processed'
		elif "+his" in body or "+info" in body:

			print "Processing HISTORY request"
			
			giftcost = float(getcost())
			print_bal = float(balance)

			if float(balance) < (len(winners)+1.0)*giftcost and len(winners) > 0:
			    print "BALANCE TOO LOW TO PAY FOR GIFTS"
			    print_bal = float(balance) - (len(winners)+1)*giftcost
			else:
                            while print_bal > giftcost:
                                print_bal -= giftcost
                                
                        hist_mes = m.history_top % (str(print_bal),str(giftcost),str(abs(float(giftcost) - float(print_bal))),len(entries),len(donor_dict))
     			for x in donor_dict.keys():
     			    hist_mes += m.history_mid % (x.split()[0],donor_dict[x])
			hist_mes += m.history_bottom % (get_todays_deposits(),count_winners())
			msg.reply(hist_mes)
 
                        print 'Request processed'
			msg.mark_as_read()
			
		 
		elif '+exit' in body and auth in authorized:
			print "Processing KILL request"
			msg.reply('Bot is shutting down')
			global kill_var
			kill_var = '9001'
			msg.mark_as_read()
			sys.exit()
			raise Exception("SHUTDOWN")
		elif '+force' in body and auth in authorized:
			print 'Processing FORCED RANDOM SEND request'
			get_winner(msg, entries)
			
		elif '+random' in body and auth in authorized:
			print "Processing RANDOM SEND request"
			giftcost = getcost()
			if float(balance) >= float(giftcost):
				get_winner(msg,entries)
			elif float(balance) < float(giftcost):
				print "BALANCE TOO LOW"
				msg.reply('Balance too low')
				msg.mark_as_read()		

		elif '+reenter' in body and auth in authorized:
			print "Processing RE-ENTRY request"
			reentree = body.split("reenter")[1].split()[0]
			reentree = r.get_redditor(reentree).name
			print reentree + " will be re-entered"
			
			add_winner(reentree,archived=True)
			add_entry(reentree)
			msg.reply(reentree + ' has been re-entered into the drawing.')
			r.send_message(reentree,'Re-entry','You have been re-entered into the drawing!' +m.footer  )
			msg.mark_as_read()
		elif "+custom" in body and auth in authorized:
		    win = custom_contest(entries)
		    reenter_link = m.reenter_link + win +")"
		    msg.reply("%s  has won the contest! Please create a post and send them a message to work out the details of the prize. \
\n \n  If they do not take the prize you can reenter them with the reenter command. \n\n [+reenter](%s " % (win, reenter_link )+win)
                    msg.mark_as_read()
                    

				
		elif '+accept' in body and auth in already_won:
		    if float(balance) > float(getcost()):
          		    msg.mark_as_read()
          		    prize = body.split("+accept ")
          		    prize = prize[1].split()[0]
          		    add_winner(auth,prize=prize,claim=True)
          		    send_prize(auth,prize)
          		    
          		    msg.reply("prize claimed!")
          		    global last_con_check
          		    last_con_check = datetime.datetime.now()+datetime.timedelta(hours=1)
          		    balance = 0.0
                    else:
                        
                        print "\n\nBALANCE TOO LOW TO FILL PRIZE OBLIGATIONS!!!!!!!\n\n"
		    
		elif '+pass' in body and auth in already_won:
		    print "proccessing pass request"
		    
		    passed_to = body.split("pass ")[1].split()[0]
		    if passed_to == 'random':
		        
		        win = get_winner(msg,entries)
		        msg.reply("You have passed on the prize to %s" % (win) +m.footer)
		        remove_winner(auth)
		        
                    else:
                        try:
                            p = r.get_redditor(passed_to).name
                            get_winner(msg,entries,p)
                            msg.reply("You have passed the prize to " + passed_to +m.footer) 
                            remove_winner(auth)
                    
                        except:
                            msg.reply("Please pick a valid redditor")
                    
                    msg.mark_as_read()
                    print 'Request processed'

		    
		else:   
		    print "Processing invalid request"
		    msg.reply("Request not understood. Please reply with +entry, +optout or +history to have your request proccessed."+m.footer)
		    msg.mark_as_read()
		 
		    print 'Request processed'
	
def custom_contest(entries):
            
                        winner = None
			print "Choosing winner for custom contest"

			
			while  True:
				if winner == None:    
				    winner = random.choice(entries)
				redditor = r.get_redditor(winner)
				redd_comments = redditor.get_comments(limit=1)
				redd_posts = redditor.get_submitted(limit=1)
				print winner + ' picked'
				verified = False
				for x in redd_comments:
					if time.time() - x.created_utc < 1209600:
						verified = True
						print 'VERIFIED'
						break
					else: 
						for y in redd_posts:
							if time.time() - y.created_utc < 1209600:
								verified = True
								print 'VERIFIED'
								
								break
							else:
								
								winner = None
								print 'NOT VERIFIED'
								continue
					        
					        winner = None
					        print 'NOT VERIFIED'
					        continue
				if verified == True:
				    break
				    

								
				time.sleep(5)
				
			print winner + ' won!'
			
		
		        new_contest(winner)
		        add_winner(winner,prize=None,claim=True,archived=False)
		        remove_entry(winner)
		        return winner
		
    
def get_winner(msg, entries,winner=None):
	choose_winner = 0
	exit_var = 'stay alive'
	if winner:
	    verified = True
	else:
	    verified = False
	       
	while exit_var != 'exit':
		line_message = ' '
		if choose_winner == 0:
			print "Choosing winner"
			if msg != 'moot':
				msg.mark_as_read()
			
			
			
			while  verified == False:
				if winner == None:    
				    winner = random.choice(entries)
				redditor = r.get_redditor(winner)
				redd_comments = redditor.get_comments(limit=1)
				redd_posts = redditor.get_submitted(limit=1)
				print winner + ' picked'
				for x in redd_comments:
					if time.time() - x.created_utc < 1209600:
						verified = True
						print 'VERIFIED'
						break
					else: 
						for y in redd_posts:
							if time.time() - y.created_utc < 1209600:
								verified = True
								print 'VERIFIED'
								break
							else:
								verified = False
								winner = None
								print 'NOT VERIFIED'
								continue
					        verified = False
					        winner = None
					        print 'NOT VERIFIED'
					        continue

								
				time.sleep(5)
			print winner + ' won!'
			
		winning_postid = r.submit(subreddit_to_post,'[Winner] %s has won the DogeGiftBot giveaway!!'% (winner),text=m.win_post % (winner, m.entry_link, m.optout_link,m.history_link))
		postLink = "http://redd.it/"+winning_postid.id 
		print postLink
		for person in authorized:
		    r.send_message(person,"New Winner!","%s has been chosen as a winner! Congratulate them [here!](%s)" % (winner, postLink))
		line_message = "An annoucement of your win has been made [here](http://redd.it/%s)   " % winning_postid.id
		r.send_message(winner, 'Congratulations!', m.winning_message % (m.accept_link,m.accept_link,m.pass_link,line_message))

		choose_winner = 0
		new_contest(winner)
		remove_entry(winner)
		return winner
		
		
def send_prize(Winner,prize):
    for x in authorized:
        r.send_message(x,'Gift Card','%s choose the %s gift card' % (Winner, prize))
        

    address = getaddress(Winner,prize)
    cost = getcost()
    r.send_message('dogetipbot',prize + ' for ' + Winner, '+withdraw %s %s doge' % (address, str(cost)))
    print address
    print Winner + ' has claimed the ' + prize + ' gift card'
    return
        

def get_dtbinfo(Text):
	global balance
	global history_hash
	global donor_dict
	text = Text
	print "Checking balance"

				
	balance = text.split()[13][2:]
	   
	print "balance: "+balance + ' DOGE'
				
				
	new_history_hash = hashlib.md5(text.encode("ascii","replace")).hexdigest()
				

	
		
	
	if new_history_hash == history_hash:
	    print "no new tips"
	
	else:
	    history_hash = new_history_hash
	    add_history_to_db(text,bot_name)
	    donor_dict = getDonors(text)
	return balance
def check_posts():
	print "Checking posts"
	submissions = r.get_subreddit(subreddit_to_post).get_new(limit=25)
	for x in submissions:
		if x.author.name in banned:
			print 'Post ID: ' + x.id 
			id = x.id
			submission = r.get_submission(submission_id = id)
			comments_list = submission.comments
			for comment in comments_list:
				if 'enter again dogegiftbot' in comment.body.lower() and comment.id not in done:
					print 'Comment ID: ' + comment.id
					print 'Processing RE-ENTRY post'
					link = 'http://redd.it/' + x.id
					r.send_message(reentry_contact,'Request for re-entry','%s has requested re-entry in [this](%s) post \n\n' % (comment.author.name, link)\
					+"[+reenter]("+m.reenter_link+comment.author.name+")")
					add_post(comment.id)
					print 'Post processed'
					break

def try_contest():
    
    giftcost = getcost()
    print "The cost of a giftcard is %s DOGE" % giftcost
    print "the current balance is %s DOGE" % balance
    winners = get_winners()

    if (len(winners)+1)*float(giftcost) <= float(balance):

        get_winner("moot",entries)
	return True
		
			
    else:
	print "Balance too low"
	return False

#bot loop

while True: 
    try:
        
        already_won = get_winners()
	entries = get_entries()
	done = get_posts()
	banned = get_banned()
	print "entries"
	print entries
	if len(already_won)>0:
	   print "winners"
	   print already_won
	if len(banned)>0:
	   print "Waiting for reentry"
	   print banned


	if datetime.datetime.now() - last_bal_check > datetime.timedelta(minutes = freq_bal_check):
	   print "Sending history request to dogetipbot"
	   r.send_message('dogetipbot','hist','+history')
	   last_bal_check = datetime.datetime.now()
	   if len(banned) > 0:
	       check_posts()

	if datetime.datetime.now() - last_con_check > datetime.timedelta(minutes = contest_freq) and \
	datetime.datetime.now() - last_his_succ < datetime.timedelta(minutes = freq_bal_check):
	    
	    last_con_check = datetime.datetime.now()
	    try_contest()
	    removed_winner = timeout_winners()
	    if removed_winner:
	       r.send_message(removed_winner,"Prize Expired", m.timeout_message)
	    
	    

	check_commands()
	savelists(entries, already_won, done)
	print 'last balance / post  check: ',
	
	print last_bal_check
	
	print "next contest check: ",
	print last_con_check + datetime.timedelta(minutes=contest_freq)
        print 
	time.sleep(30)

    except KeyboardInterrupt:
 	savelists(entries, already_won, done)
 	sys.exit()
    except:
 	savelists(entries, already_won, done)
 	if kill_var == '9001':
 	      while True:
 	          sys.exit()
 	          time.sleep(20)
 	print "exception traceback"
 	traceback.print_exc() 
 	print 'Please send the above information to the author of this program'
 	time.sleep(10)
 	continue 
