class dogegiftbotmessages():
    def __init__(self):
        self.win_post = """The winner is...   
 **/u/%s**! Congratulations!  
 You are the winner of this round of a $25 gift-card purchased with Dogecoin!  
 A PM has been sent to you with more details.  
 We would like to thank all members of the community here at /r/dogecoin. Without you, this wouldn't be possible because this is a crowd funded gift bot.  
 A special thank you to the folks at [eGifter](http://www.egifter.com) for supplying the large selection of cards. Check out their site
and maybe you might see a gift card you or someone you know might like.  :)  And of course they do accept doge coins for payment.  
 If you would like to participate in dogegiftbot giveaways, simply click [here](%s).  
 If you want to opt-out of these giveaways, click [here](%s).  
 If you would like to see some information on the current round, click [here](%s).  
 **THIS MESSAGE IS A TEST. PLEASE DISREGARD IT.**   
 --/u/dogegiftbot Team  
 
 ^Concept ^by ^/u/bigdred777 ^and ^/u/TheLobstrosity  
 ^Coded ^by ^/u/PieMan2201 ^through ^[bots4doge.com](http://www.bots4doge.com)   
 ^This ^bot ^is ^run ^on ^community ^donations. ^Donate ^by ^tipping ^through ^/u/dogetipbot ^or ^sending ^Dogecoin ^to ^D8vVxYMKkmUKRpmG82Z6FCfwZWC4rgVT5w"""
 #winner, entry link , optout link , history link
 
        self.entry_link="http://www.reddit.com/message/compose?to=dogegiftbot&subject=enter&message=%2Bentry"
        self.optout_link = 'http://www.reddit.com/message/compose?to=dogegiftbot&subject=exit&message=%2Boptout'
        self.history_link = 'http://www.reddit.com/message/compose?to=dogegiftbot&subject=history&message=%2Bhistory'
        self.winning_message = '''You have won a dogegiftbot giveaway!   
Reply with "accept [name of gift-card] dogegiftbot" to claim your gift-card from [egifter.com](https://www.egifter.com/giftcards) 
Simply go to their website and pick what company you would like your gift card from. Example, if you were to pick Amazon as your the
card you would like for your gift. The accept command would look like this "[+accept](%s) Amazon dogegiftbot" 
If you would like to pass the gift to another random person, reply with "pass random dogegiftbot".  
If you would like to pass to a certain Redditor who is in the giveaway,  then reply with "pass [name of redditor] dogegiftbot" to pass it to a specific redditor.  
You have 72 hours (3 days) to reply to this message. If you have not replied by then, a new winner will be picked.    
%s
^This ^bot ^is ^run ^on ^community ^donations. ^Donate ^by ^tipping ^through ^/u/dogetipbot ^or ^sending ^Dogecoin ^to ^D8vVxYMKkmUKRpmG82Z6FCfwZWC4rgVT5w    
THIS IS A TEST. PLEASE FOLLOW THE INSTRUCTIONS EVEN THOUGH YOU WILL NOT BE REWARDED.'''
        self.accept_link = "http://www.reddit.com/message/compose?to=dogegiftbot&subject=enter&message=%2Baccept%20PRIZE"