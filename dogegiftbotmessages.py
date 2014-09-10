# -*- coding: utf-8 -*-
class dogegiftbotmessages():
    def __init__(self):
        self.footer = u" \n \n^This ^bot ^is ^run ^on ^community ^donations. ^Donate ^by ^tipping ^through ^/u/dogetipbot ^or ^sending ^Dogecoin ^to ^+/u/dogetipbot ^@D8vVxYMKkmUKRpmG82Z6FCfwZWC4rgVT5w ^AMOUNT ^doge ^verify"
        self.win_post = u"""  
 **/u/%s, congratulations!**  
 You are the proud new owner of a $25 gift-card purchased with Ð! A PM has been sent to you with more details.  
 -We would like to thank all members of the community here at /r/dogecoin and everyone who donated in this round. Without you, this wouldn't be possible because this is a crowd funded gift bot.  
 -A special thank you to the folks at [eGifter](http://www.egifter.com) for supplying the large selection of cards. Check out their site
and maybe you might see a gift card you or someone you know might like.  :)  And of course they do accept doge coins for payment.  
 -It's totally free to enter the DogeGiftBot giveaway! If you would like to enter the giveaway, simply click [here](%s).
 -If you would like to see information on the current round, click [here](%s).  
 -www.dogegiftbot.com  Check out the new website! <3
 
 --/u/dogegiftbot Team  
 
 ^Concept ^by ^/u/bigdred777 ^and ^/u/TheLobstrosity  
 ^Bot ^version ^1.0 ^programmed ^by ^/u/PieMan2201 ^through ^[bots4doge.com](http://www.bots4doge.com)
 ^Bot ^version ^1.1. ^upgrade ^programmed ^by ^/u/Doomhammer458
 ^DogeGiftBot ^Hosting ^is ^provided ^by ^https://nanobit.pl/.
""" +self.footer
 #winner, entry link , optout link , history link
 
        self.entry_link="http://www.reddit.com/message/compose?to=dogegiftbot&subject=enter&message=%2Bentry"
        self.optout_link = 'http://www.reddit.com/message/compose?to=dogegiftbot&subject=optout&message=%2Boptout'
        self.history_link = 'http://www.reddit.com/message/compose?to=dogegiftbot&subject=history&message=%2Bhistory'
        self.winning_message = '''You have won a dogegiftbot giveaway!   
-Reply with "+accept [name of gift-card]" to claim your gift-card from [egifter.com](https://www.egifter.com/giftcards) 
Simply go to their website and pick what company you would like your gift card from. Example, if you were to choose Amazon as your card that
you would like for your gift then the accept command would look like this "%s Amazon " 
Once you send the accept command it can take a few minutes to get your card sent to your reddit inbox. If it does not come within
an hour then contact /u/bigdred777 or /u/TheLobstrosity so that we can make sure you get your card.
-If you would like to pass the gift to another random person, reply with "+pass random".  
-If you would like to pass to another Redditor, then reply with "+pass [name of redditor] " to pass it to a specific redditor. Redditor must be in giveaway to win. 
-You have 72 hours (3 days) to reply to this message. If you have not replied by then, a new winner will be picked.
*To re-enter the giveaway you will need to post a new link thread with a picture of something you bought with your gift card, 
also write down on a piece of paper your reddit username and include that in the picture. Then simply comment in your thread and
include the "+enter again" command. A admin will then manually verify your picture and then will add you back into the giveaway.
You will receive conformation of your re-entry.

\n \n %s \n \n %s \n \n %s

''' +self.footer

        self.accept_link = "[+accept](http://www.reddit.com/message/compose?to=dogegiftbot&subject=accept&message=%2Baccept%20PRIZE)"  
        self.pass_link = " [+pass](http://www.reddit.com/message/compose?to=dogegiftbot&subject=pass&message=%2Bpass%20RANDOM)"
        self.history_top = '''My balance is %s DOGE  
 My goal is %s DOGE  
 I need %s DOGE to reach my goal. 
 \nThere are %i entries. 
 \nThe last %i donors are:
'''
        # balance, cost, balance-cost, len (donors)
        self.history_mid = '\n * %s - %s doge'
        #donor, donation
        
        self.history_bottom = '''\n\n
Anonymous donations have contributed %.2f doge today.\n
There has been a total of %i winners.\n
To donate, you can either tip me using /u/dogetipbot,  
or send Dogecoin to D8vVxYMKkmUKRpmG82Z6FCfwZWC4rgVT5w.  
If you send Dogecoin from your wallet your name will show up as "anonymous".  
^Concept ^by ^/u/bigdred777 ^and ^/u/TheLobstrosity  

^Programmed ^by ^/u/PieMan2201 ^through ^bots4doge.com''' 
        self.reenter_link =  'http://www.reddit.com/message/compose?to=dogegiftbot&subject=reenter&message=%2Breenter%20'
        
        
        self.timeout_message = "Your prize has expired and will be passed to another entrant.  \n\n \
you can renter with the following link \n\n [+entry](%s)" % (self.entry_link)
        
        


