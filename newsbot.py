from telegram.ext import Updater, MessageHandler, CommandHandler, Filters
from watson_developer_cloud import ConversationV1
import json
import requests

context = None


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    print('Received /start command')
    update.message.reply_text('Hi!')


def help(bot, update):
    print('Received /help command')
    update.message.reply_text('Help!')


def message(bot, update):
    print('Received an update')
    global context

    conversation = ConversationV1(username='161a18e1-8ddc-404c-894b-26470e295d90',  # TODO
                                  password='d07Jb1MQduZM',  # TODO
                                  version='2018-02-16')

    # get response from watson
    response = conversation.message(
        workspace_id='cb90b423-b0c4-45b5-9ee2-002f8ebdd6de',  # TODO
        input={'text': update.message.text},
        context=context)
    print(json.dumps(response, indent=2))
    
    context = response['context']
    print(context)

    # build response
    resp = ''
    ret=''
    esp=''
    es=''
    for i in response['intents']:
        	es += i['intent']
    if es!='Bot_Control_Approve_Response':
	for text in response['output']['text']:
        	resp += text
    	update.message.reply_text(resp)
    else: 
	 for text in response['output']['text']:
        	resp += text
         count=response['context']['count']
	 
         category=response['context']['category']
         n=requests.get('https://newsapi.org/v2/top-headlines?country='+count+'&category='+category+'&apiKey=9ef6f45b13b94839b709d56d1b728ab6')
	 obj=n.json()
	 ret+=str(obj['articles'][10]['url'])
	 update.message.reply_text(resp+'\n'+'\n'+ret)
    
	



    
    


def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater('639931768:AAE4yJYO_HlMG7QL4RPwa0c4tScm3A-bQo4')  #TODO

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, message))

    # Start the Bot
    updater.start_polling()

    # Block until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
