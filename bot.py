
import requests
import feedparser
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import threading
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
logger = logging.getLogger(__name__)



BOT_TOKEN = "here goes telegram  api" #ask @botfather in telegram for this variable not me
CHANNEL_ID = '@srtas234' # @bot_channel_name any channel/ group name
FEED_URL = ['https://www.indiatoday.in/rss/home'] # https://something.com/feeds/rss.xml


def send_message(message):
    requests.get(f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHANNEL_ID}&text={message}')

def main():
    global FEED_URL
    d=FEED_URL
    for i in d:
    	rss_feed = feedparser.parse(i)
    	send_message(rss_feed.entries[-1].links[0].href)
    threading.Timer(1000, main).start()

def add(update, context):
	global FEED_URL
	try:
		context.args[0]
	except:
		update.effective_message.reply_text(
    		"ERROR: The format needs to be a list seprated by spaces: /add (longpress)  http://www.URL.com http://www.link.com \n single input list also works ")
		raise
	for f in context.args:
		try:
			rss_d = feedparser.parse(f)
			if rss_d.entries[0]['title']:
				if f in FEED_URL:
					update.effective_message.reply_text(" its already added!!")
					continue
				FEED_URL.append(f)
				update.effective_message.reply_text("added \nRSS: %s" % (context.args[0]))
		except:
			update.effective_message.reply_text(
				"ERROR: The link does not seem to be a RSS feed or is not supported")

def echo(update, context):
        """Echo the user message."""
        global FEED_URL
        temp=FEED_URL
        FEED_URL=update.message.text.split()[0]
        try:
            d=feedparser.parse(FEED_URL)
            if d.entries==[]:
                FEED_URL=temp
                raise
            update.message.reply_text('updated link is '+FEED_URL)

        except:
            FEED_URL=temp
            update.message.reply_text('its invalid')

def dmain():
        """Start the bot."""
        # Create the Updater and pass it your bot's token.
        # Make sure to set use_context=True to use the new context based callbacks
        # Post version 12 this will no longer be necessary
        updater = Updater(BOT_TOKEN, use_context=True)

        # Get the dispatcher to register handlers
        dp = updater.dispatcher
        dp.add_handler(CommandHandler("add", add))
        dp.add_handler(MessageHandler(Filters.text, echo))
        # log all errors

        # Start the Bot 
        updater.start_polling()

        # Run the bot until you press Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT. This should be used most of the time, since
        # start_polling() is non-blocking and will stop the bot gracefully.
        updater.idle()
       

if __name__ == "__main__":
    main()
    dmain()

   
