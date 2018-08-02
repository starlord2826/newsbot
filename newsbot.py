from telegram.ext import Updater, MessageHandler, CommandHandler, Filters
from watson_developer_cloud import ConversationV1
import json
import requests
from gtts import gTTS
import os

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
        workspace_id='0cc6da39-2d3a-4848-807b-bac40520c026',  # TODO
        input={'text': update.message.text},
        context=context)
    print(json.dumps(response, indent=2))

    context = response['context']

    # build response
    resp = ''
    categ = ''
    ret = ''
    esp = ''
    res = ''
    es = ''
    source = ''
    rett = ''
    temp = ''
    temp_min = ''
    temp_max = ''

    for text in response['intents']:
        es += text['intent']

    if es != 'Bot_Control_Approve_Response' and es != 'final' and es != 'abcd':
        for text in response['output']['text']:
            resp += text
            update.message.reply_text(resp)
    if es == 'abcd':
        res = response['input']['text']
        print(2)
        n = requests.get(
            'https://newsapi.org/v2/everything?q=' + res + '&sortBy=popularity&apiKey=85c3ead119524a58899bde57a9e38032')
        obj = n.json()
        re = int(obj['totalResults'])
        ret = ''
        ret += str(obj['articles'][1]['url'])
        print(ret)
        update.message.reply_text(ret)
    elif es != 'final' and es == 'Bot_Control_Approve_Response':
        # update.message.reply_text("http://127.0.0.1:5000/")
        for text in response['output']['text']:
            resp += text
            count = response['context']['count']
            category = response['context']['category']
            n = requests.get(
                'https://newsapi.org/v2/top-headlines?country=' + count + '&category=' + category + '&apiKey=0b2bb070c6074bcfa178b18b35a69ba9')
            obj = n.json()
            # ret+=str(obj['articles'][1]['url'])
            print(7)
            for i in range(0, 10):
                ret += str(i + 1) + ':  ' + str(obj['articles'][i]['title']) + '\n' + '\n'
                update.message.reply_text(resp + '\n' + '\n' + ret)
    elif es == '':
        for text in response['output']['text']:
            resp += text
            res = response['input']['text']
            print(res)
            we = response['input']['text']
            n = requests.get(
                'http://api.openweathermap.org/data/2.5/weather?q=' + we + ',ru&appid=ac7c75b9937a495021393024d0a90c44&units=metric')
            obj = n.json()
            ret = ''
            ret += str(obj['weather'][0]['description'])
            temp += str(obj['main']['temp'])
            temp_min += str(obj['main']['temp_min'])
            temp_max += str(obj['main']['temp_max'])
            print(ret)
            update.message.reply_text(
                'Description :' + ret + '\nTemperature :' + temp + '\nMinimum Temperature :' + temp_min + '\nMaximum Temperature :' + temp_max)
    else:
        num = response['context']['number']
        count = response['context']['count']
        category = response['context']['category']
        print(num)
        n = requests.get(
            'https://newsapi.org/v2/top-headlines?country=' + count + '&category=' + category + '&apiKey=0b2bb070c6074bcfa178b18b35a69ba9')
        obj = n.json()
        # source='we have got this news from '+str(obj['articles'][1323]['source']['name'])+'\n'+'\n'
        ret += str(obj['articles'][num - 1]['url'])
        update.message.reply_text(ret)
        rett += str(obj['articles'][num - 1]['title'])
        tts = gTTS(text=rett, lang='en')
        tts.save("good.mp3")
        os.system("cvlc good.mp3")


# update.message.reply_audio(audio='/home/sandesh/projects/project/newsbot/good.mp3')
# bot.send_audio(chat_id=systbotbot,  audio=open('/home/sandesh/projects/project/newsbot/good.mp3', 'rb'))

def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater("630960342:AAGOpUpEw10u9Vd6gWaVUx5c4Fuy1unUbOc")

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
