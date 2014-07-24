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
r = praw.Reddit(user_agent='dogegiftbot version 0.2')

###### config section ############
bot_name = "multisigtest1"
#authorized admins
authorized = ['Doomhammer458']
#login info
r.login()                  #leave blank for praw config
reentry_contact = "Doomhammer458"
subreddit_to_post = "dogetrivia"
###### config section ############


# Created by /u/PieMan2201 through bots4doge.com
    


bot_name = bot_name.lower()
winner_count = 0

print 'LOGIN SUCCESS'
kill_var = '321'
winners = []
msgcheck = 0

balance = 0
for msg in r.get_unread(limit=None):
	msg.mark_as_read()
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
winning_message = '''You have won a dogegiftbot giveaway!   
Reply with "accept [name of gift-card] dogegiftbot" to claim a gift-card from [egifter.com](https://www.egifter.com/giftcards)  
If you would like to pass the gift, reply with "pass random dogegiftbot" to pass it to a random person.  
Reply with "pass [name of redditor] dogegiftbot" to pass it to a specific redditor.  
You have 72 hours (3 days) to reply to this message. If you have not replied by then, a new winner will be picked.  
%s
^This ^bot ^is ^run ^on ^community ^donations. ^Donate ^by ^tipping ^through ^/u/dogetipbot ^or ^sending ^Dogecoin ^to ^D8vVxYMKkmUKRpmG82Z6FCfwZWC4rgVT5w    
THIS IS A TEST. PLEASE FOLLOW THE INSTRUCTIONS EVEN THOUGH YOU WILL NOT BE REWARDED.'''


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

		if '+ent' in body:
			print "Processing ENTRY request"
			msg.mark_as_read()
			user = r.get_redditor(auth)
			comkarm = user.comment_karma
			linkkarm = user.link_karma
			if int(comkarm) > 49 or int(linkkarm) > 49:
				if auth not in entries and auth not in already_won:
					add_entry(auth)
					msg.reply('''You have been entered into the giveaway!  
 ^This ^bot ^is ^run ^on ^community ^donations. ^Donate ^by ^tipping ^through ^/u/dogetipbot ^or ^sending ^Dogecoin ^to ^D8vVxYMKkmUKRpmG82Z6FCfwZWC4rgVT5w  ''')
					print auth + ' has entered'
				else:
					msg.reply('Silly shibe! You can only enter once.')
					print auth + ' is a meatbag'
			else:
				print auth + ' does not meet requirements'
				msg.reply("I'm sorry, but you do not have sufficient comment karma to register. You need at least 50 comment karma to enter.")

			
			print 'Request processed'
			
		elif '+opt'in body and auth in entries:
			print 'Processing OPT-OUT request'
			msg.mark_as_read()
			remove_entry(auth)
			msg.reply('''You have been removed from the giveaway.  
 ^This ^bot ^is ^run ^on ^community ^donations. ^Donate ^by ^tipping ^through ^/u/dogetipbot ^or ^sending ^Dogecoin ^to ^D8vVxYMKkmUKRpmG82Z6FCfwZWC4rgVT5w  ''')
			
			print 'Request processed'
		elif '+his' in body:
			print "Processing HISTORY request"
			
			giftcost = getcost()

                        donors = []
                        donations = []
     			for x in donor_dict.keys():
        			donors.append(x)
        			donations.append(donor_dict[x])
			print donors 
			print donations
			msg.reply('''My balance is %s DOGE  
 My goal is %s DOGE  
 I need %s DOGE to reach my goal.  
 The last 10 donors are:
 
 * %s - %s doge
 * %s - %s doge
 * %s - %s doge
 * %s - %s doge
 * %s - %s doge
 * %s - %s doge
 * %s - %s doge
 * %s - %s doge
 * %s - %s doge
 * %s - %s doge

 To donate, you can either tip me using /u/dogetipbot,  
 or send Dogecoin to D8vVxYMKkmUKRpmG82Z6FCfwZWC4rgVT5w.  
 If you send Dogecoin from your wallet, you will not be featured as a donor.  
 ^Concept ^by ^/u/bigdred777 ^and ^/u/TheLobstrosity  
 ^Programmed ^by ^/u/PieMan2201 ^through ^bots4doge.com''' % (balance,giftcost,str(float(giftcost) - float(balance)), donors[0], 
																													donations[0], 
																													donors[1], 
																													donations[1], 
																													donors[2], 
																													donations[2], 
																													donors[3],
																													donations[3],
																													donors[4],
																													donations[4],
																													donors[5],
																													donations[5],
																													donors[6],
																													donations[6],
																													donors[7], 
																													donations[7],
																													donors[8],
																													donations[8],
																													donors[9],
																													donations[9]))
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
		elif 'force send random dogegiftbot' in body and auth in authorized:
			print 'Processing FORCED RANDOM SEND request'
			get_winner(msg, entries)
		elif 'reenter' in body and 'dogegiftbot' in body and auth in authorized:
			print "Processing RE-ENTRY request"
			reentree = msg.body[8:-12]
			print reentree + " will be re-entered"
			add_entry(reentree)
			remove_winner(reentree)
			msg.reply(reentree + ' has been re-entered into the drawing.')
			r.send_message(reentree,'Re-entry','''You have been re-entered into the drawing!  
 ^This ^bot ^is ^run ^on ^community ^donations. ^Donate ^by ^tipping ^through ^/u/dogetipbot ^or ^sending ^Dogecoin ^to ^D8vVxYMKkmUKRpmG82Z6FCfwZWC4rgVT5w  ''')
			msg.mark_as_read()
		
		else:
		    print "Processing invalid request"
		    msg.reply("Request not understood. Please reply with +entry, +optout or +history to have your request proccessed.\n \n \
^This ^bot ^is ^run ^on ^community ^donations. ^Donate ^by ^tipping ^through ^/u/dogetipbot ^or ^sending ^Dogecoin ^to ^D8vVxYMKkmUKRpmG82Z6FCfwZWC4rgVT5w")
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
		winning_postid = r.submit(subreddit_to_post,'[Winner] DogeGiftBot Winner!',text="""The winner is...   
 **/u/%s**! Congratulations!  
 They have been picked as the winner of this round, and have the option of selecting a $25 gift-card purchased with Dogecoin!  
 A PM has been sent to the winner with more details.  
 We would like to thank all members of the community here at /r/dogecoin. Without you, this wouldn't be possible.  
 A special thank you to the folks at [eGifter](http://www.egifter.com) for supplying the large selection of cards. Without them, this little dream would have never come true.  
 If you would like to participate in dogegiftbot giveaways, simply click [here](%s).  
 If you want to opt-out of these giveaways, click [here](%s).  
 If you would like to see some information on the current round, click [here](%s).  
 **THIS MESSAGE IS A TEST. PLEASE DISREGARD IT.**   
 --/u/dogegiftbot Team  
 
 ^Concept ^by ^/u/bigdred777 ^and ^/u/TheLobstrosity  
 ^Coded ^by ^/u/PieMan2201 ^through ^[bots4doge.com](http://www.bots4doge.com)   
 ^This ^bot ^is ^run ^on ^community ^donations. ^Donate ^by ^tipping ^through ^/u/dogetipbot ^or ^sending ^Dogecoin ^to ^D8vVxYMKkmUKRpmG82Z6FCfwZWC4rgVT5w""" % (winner, 
									'http://www.reddit.com/message/compose?to=dogegiftbot&subject=enter&message=%2Bentry',
									'http://www.reddit.com/message/compose?to=dogegiftbot&subject=exit&message=%2Boptout',
									'http://www.reddit.com/message/compose?to=dogegiftbot&subject=history&message=%2Bhistory')
										)
		print winning_postid.id 
		line_message = "An annoucement of your win has been made [here](http://redd.it/%s)   " % winning_postid.id
		r.send_message(winner, 'Congratulations!', winning_message % line_message)
		choice = 0
		timer = 0
		choose_winner = 0
		while choice == 0 and timer < 8640:
			msgs = r.get_unread(limit=None)
			for msg in msgs:
				if 'accept' in msg.body.lower() and 'dogegiftbot' in msg.body.lower() and msg.author.name == winner and msg.was_comment == False:
					msg.mark_as_read()
					forward = str(msg.body.lower())[:-12]
					forward_t = str(forward)[7:]
					for x in authorized:
						r.send_message(x,'Gift Card','%s choose the %s gift card' % (msg.author.name, forward_t))
					choice = 'boo'
					msg.reply('''You choose the %s giftcard. If you would like to be re-entered into the giveaway, please create a submission that contains a link to a picture of your giftcard.  
 Then, create a comment on that submission that contains the text `enter again dogegiftbot`.  
 ^This ^bot ^is ^run ^on ^community ^donations. ^Donate ^by ^tipping ^or ^sending ^Dogecoin ^to ^D8vVxYMKkmUKRpmG82Z6FCfwZWC4rgVT5w  ''' % forward_t)
					address = getaddress(msg.author.name,forward_t)
					cost = getcost()
					r.send_message('dogetipbot',forward_t + 'for' + msg.author.name, '+withdraw %s %s doge' % (address, str(cost)))
					print address
					if msg.author.name in entries:
						remove_entry(msg.author.name)
					add_winner(msg.author.name)
					print winner + ' has claimed the ' + forward_t + ' gift card'
					exit_var = 'exit'
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
def get_dtbinfo():
	global first_run
	global balance
	text = None
	print "Checking balance"
	r.send_message('dogetipbot','moot','+history')
	print 'sent message'
	if first_run == 0:
		balance_old = balance
		text_old = text
	else:
		balance_old = '9001'
		text_old = '/u/PieMan2201'
	first_run = 0
	balance = 0
	balance_counter = 0
	while balance == 0 and balance_counter < 18:
		msgs = r.get_unread()
#		print 'moot'
		for x in msgs:
#			print 'moot2'
			if x.author.name == 'dogetipbot' and 'here are your last' in x.body.lower():
				
				balance = x.body.split()[13][2:]
				print "balance: "+balance + ' DOGE'
				x.mark_as_read()
				text = x.body.lower()
				
		balance_counter += 1
		if balance_counter == 18:
			print 'Time limit exceeded, balance update FAILED'
			balance = balance_old
			text = text_old
		if balance > 0:
		    break
		time.sleep(20)
	global donor_dict
	
	donor_dict = getDonors(text)
def check_posts():
	print "Checking posts"
	submissions = r.get_subreddit('dogecoin').get_new(limit=25)
	for x in submissions:
		if x.author.name in already_won:
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



#bot loop

while True: 
    try:
        
        already_won = get_winners()
	entries = get_entries()
	done = get_posts()
	print "entries"
	print entries
	print 'A giftcard costs ' + str(getcost()) + ' doge' 
	if datetime.datetime.now() - last_bal_check > datetime.timedelta(minutes = 10):
	   get_dtbinfo()
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
