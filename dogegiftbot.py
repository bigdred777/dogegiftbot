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
m = dogegiftbotmessages()
r = praw.Reddit(user_agent='dogegiftbot version 0.2')

###### config section ############
bot_name = "dogemultisigescrow"
#authorized admins
authorized = ['Doomhammer458']
#login info
r.login()                  #leave blank for praw config
reentry_contact = "Doomhammer458"
subreddit_to_post = "dogetrivia"
freq_bal_check = 10 # time in minute
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
repcount = 0
last_bal_check = datetime.datetime.now() - datetime.timedelta(days=5)
postcheck = 0
first_run = 1
done = get_posts()
donors = []
donations = []
donor_dict = {}
lower_body = 'bnipdsn'


already_won = get_winners()


print entries
print already_won
print done
def getDonors(text):
        
	text2 = text.replace('|',' ').encode("ascii","replace")
	dict = {}
	text3 = StringIO.StringIO(text2)
	counter = 0

	for line in text3:
	        
	        if "**/u/"+bot_name+"**" in line:
	           
	            
	            if line.split()[0] == "tip":
	                  
	                

		    
		         if line.split()[3] == '**/u/'+bot_name+'**' and line.split()[1] == "?"and counter <10:
		         	        

		         	        
		        	if line.split()[2] not in dict.keys():
		        		        
		           	  dict[line.split()[2]] = float(line.split()[6])
		           	  counter += 1
		        	elif line.split()[2] in dict.keys():
                                    dict[line.split()[2]] = dict[line.split()[2]] + float(line.split()[6])
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
	f = urllib.urlopen('http://www.coinmill.com/USD_XDG.html')
	s = f.read()
	for x in s.split():
		if '1.00' == x:
			index = s.split().index(x) 
			cost = int(s.split()[index + 2]) * 26
			cost_two = cost + 100
	return cost_two
def check_commands():
	print 'Checking messages'
	msgs = r.get_unread(limit=None)
	for msg in msgs:
	        if type(msg) != praw.objects.Message:
	            msg.mark_as_read()
	            print "NEW comment reply: ",
	            print msg
	            continue
	        
	        entries = get_entries()
		body = msg.body.lower()
		id = msg.id
		auth = msg.author.name
		if auth== "dogetipbot":
		    print "dogetipbot message"
		    if 'here are your last' in body:
                        get_dtbinfo(body)
                        msg.mark_as_read()
		    else:
		        msg.mark_as_read()
		       
		        print body
		        print
		        continue

		
		elif '+ent' in body:
			print "Processing ENTRY request"
			msg.mark_as_read()
			user = r.get_redditor(auth)
			comkarm = user.comment_karma
			linkkarm = user.link_karma
			if int(comkarm) > 49 or int(linkkarm) > 49:
				if auth not in entries and (auth not in already_won or auth not in banned):
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
		elif '+his' in body:
		        if auth == "dogetipbot":
		            msg.mark_as_read()
		            continue
			print "Processing HISTORY request"
			
			giftcost = float(getcost())
			print_bal = float(balance)
			while print_bal > giftcost:
			    print_bal -= giftcost
                        hist_mes = m.history_top % (str(print_bal),str(giftcost),str(abs(float(giftcost) - float(print_bal))),len(donor_dict))
     			for x in donor_dict.keys():
     			    hist_mes += m.history_mid % (x,donor_dict[x])
			hist_mes += m.history_bottom 
			msg.reply(hist_mes)
 
                        print 'Request processed'
			msg.mark_as_read()
			
		 
		elif 'exit' in body and auth in authorized:
			print "Processing KILL request"
			msg.reply('Bot is shutting down')
			global kill_var
			kill_var = '9001'
			msg.mark_as_read()
			sys.exit()
			raise Exception("SHUTDOWN")
		elif 'force send random dogegiftbot' in body and auth in authorized:
			print 'Processing FORCED RANDOM SEND request'
			get_winner(msg, entries)
			
		elif 'send random dogegiftbot' in body and auth in authorized:
			print "Processing RANDOM SEND request"
			giftcost = getcost()
#			giftcost = 10
			if float(balance) >= float(giftcost):
				get_winner(msg,entries)
			elif float(balance) < float(giftcost):
				print "BALANCE TOO LOW"
				msg.reply('Balance too low')
				msg.mark_as_read()		

		elif 'reenter' in body and 'dogegiftbot' in body and auth in authorized:
			print "Processing RE-ENTRY request"
			reentree = msg.body[8:-12]
			print reentree + " will be re-entered"
			
			add_winner(reentree,archived=True)
			add_entry(reentree)
			msg.reply(reentree + ' has been re-entered into the drawing.')
			r.send_message(reentree,'Re-entry','You have been re-entered into the drawing!' +m.footer  )
			msg.mark_as_read()
		
		elif '+accept' in body and auth in already_won:
		    prize = body.split("+accept ")
		    prize = prize[1].split()[0]
		    send_prize(auth,prize)
		    add_winner(auth,prize=prize,claim=True)
		    msg.mark_as_read()
		    
		    

		    
		else:   
		    print "Processing invalid request"
		    msg.reply("Request not understood. Please reply with +entry, +optout or +history to have your request proccessed."+m.footer)
		    msg.mark_as_read()
		 
		    print 'Request processed'
		return True
def get_winner(msg, entries):
	choose_winner = 0
	exit_var = 'stay alive'
	passer = 'I am IRON MAN!'
	while exit_var != 'exit':
		line_message = ' '
		if choose_winner == 0:
			print "Choosing winner"
			if msg != 'moot':
				msg.mark_as_read()
			rand = random.randrange(0,len(entries))
			winner = entries[rand]
			verified = False
			while winner == passer or verified == False:
				rand = random.randrange(0,len(entries))
				winner = entries[rand]
				redditor = r.get_redditor(winner)
				redd_comments = redditor.get_comments(limit=1)
				redd_posts = redditor.get_submitted(limit=1)
				print winner + ' picked'
				for x in redd_comments:
					if time.time() - x.created_utc < 1209600:
						verified = True
						print 'VERIFIED'
					else: 
						for y in redd_posts:
							if time.time() - y.created_utc < 1209600:
								verified = True
								print 'VERIFIED'
							else:
								verified = False
								print 'NOT VERIFIED'
				time.sleep(5)
			print winner + ' won!'
		winning_postid = r.submit(subreddit_to_post,'[Winner] DogeGiftBot Winner!',text=m.win_post % (winner, m.entry_link, m.optout_link,m.history_link))
		print "http://redd.it/"+winning_postid.id 
		line_message = "An annoucement of your win has been made [here](http://redd.it/%s)   " % winning_postid.id
		r.send_message(winner, 'Congratulations!', m.winning_message % (m.accept_link,line_message))

		choose_winner = 0
		new_contest(winner)
		remove_entry(winner)
		return 
		
		
def send_prize(Winner,prize):
    for x in authorized:
        r.send_message(x,'Gift Card','%s choose the %s gift card' % (Winner, prize))
        

    address = getaddress(Winner,prize)
    cost = getcost()
    r.send_message('dogetipbot',prize + 'for' + Winner, '+withdraw %s %s doge' % (address, str(cost)))
    print address
    print Winner + ' has claimed the ' + prize + ' gift card'
    return
        
    """

					
					
				elif 'pass random dogegiftbot' == msg.body.lower() and msg.author.name == winner and msg.was_comment == False:
					lower_body = msg.body.lower()
					choice = 'boo'
					print winner + ' has passed randomly'
					msg.reply('''The gift has been passed on.  
 ^This ^bot ^is ^run ^on ^community ^donations. ^Donate ^by ^tipping ^or ^sending ^Dogecoin ^to ^D8vVxYMKkmUKRpmG82Z6FCfwZWC4rgVT5w  ''')
					msg.mark_as_read()
					passer = msg.author.name
				elif 'pass' in msg.body.lower() and 'dogegiftbot' in msg.body.lower() and 'pass random dogegiftbot' not in msg.body.lower() and msg.author.name == winner and msg.was_comment == False:
					lower_body = msg.body.lower()
					choice = 'boo'
					winner2 = winner
					msg.mark_as_read()
					choose_winner = 'not 0'
					winner = lower_body[5:-12]
					msg.reply('''You have passed the gift to %s    
 ^This ^bot ^is ^run ^on ^community ^donations. ^Donate ^by ^tipping ^or ^sending ^Dogecoin ^to ^D8vVxYMKkmUKRpmG82Z6FCfwZWC4rgVT5w  ''' % winner)					
					print winner2 + ' has passed to ' + winner
			check_commands()
			timer += 1
			if timer == 8640:
				r.send_message(winner, 'Sorry!', "We regret to inform you that you're time has expired. The gift will be passed to another participant.")
				choose_winner = 0
			time.sleep(30)
			"""
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
	    return
	else:
	    history_hash = new_history_hash
	    add_history_to_db(text,bot_name)
	    donor_dict = getDonors(text)
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
					r.send_message(reentry_contact,'Request for re-entry','%s has requested re-entry in [this](%s) post.' % (comment.author.name, link))
					add_post(comment.id)
					print 'Post processed'
					break



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
	   print "Waiting for rentry"
	   print banned

	print 'A giftcard costs ' + str(getcost()) + ' doge' 
	if datetime.datetime.now() - last_bal_check > datetime.timedelta(minutes = freq_bal_check):
	   print "Sending history request to dogetipbot"
	   r.send_message('dogetipbot','hist','+history')
	   last_bal_check = datetime.datetime.now()

	
	if repcount < 120:
		if postcheck == 6:
			check_posts()
			postcheck = 0
			
		if msgcheck == 0:
			check_commands()
			savelists(entries, already_won, done)
			msgcheck = 0
		
		
		repcount += 1
		postcheck += 1
		print 'last balance check: ',
		print last_bal_check
		print 'rep: ' + str(repcount)
		print 'pos: ' + str(postcheck)
		time.sleep(30)
	elif repcount >= 120:
		giftcost = getcost()
#		giftcost = 10
		print "The cost of a giftcard is %s DOGE" % giftcost
		print "the current balance is %s DOGE" % balance
		if float(giftcost) <= float(balance):
			get_winner('moot',entries)
			repcount = 0
		elif float(giftcost) > float(balance):
			print "Balance too low"
			repcount = 0
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
