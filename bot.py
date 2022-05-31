from telegram.ext import *
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import requests
import pyshorteners
import bitly_api

API_KEY = '[BOT API KEY]'


def start(update, context):
    update.message.reply_text('Hey I\'m a link shortner bot.\n\nSend /help to know more!')


def help(update, context):
    update.message.reply_text('Send /short [link you want to short]\n\nExample:\n    /short https://www.google.com')


def short(update, context):
    global getLink

    btn = [[InlineKeyboardButton('bit.ly', callback_data='bitly')], [InlineKeyboardButton('cutt.ly', callback_data='cuttly')], [InlineKeyboardButton('tiny.com', callback_data='tinycom')]]

    x = str(update.message.text).lower()
    getLink = x[7:]

    update.message.reply_text('Choose a type:', reply_markup=InlineKeyboardMarkup(btn))
    
def queryHandler(update, context):
    query = update.callback_query.data
    update.callback_query.answer()

    if 'bitly' in query:
        ACCESS_TOKEN = '[BITLY ACCESS TOKEN]'
        connection = bitly_api.Connection(access_token=ACCESS_TOKEN)
        shortlink = connection.shorten(getLink).get('url')
        longlink = connection.shorten(getLink).get('long_url')

        update.callback_query.message.edit_text(f'Long link :- {longlink}\n\nShorted link :- {shortlink}\n\nLink type :- bit.ly')
    elif 'cuttly' in query:
        API_KEY = '[CUTTLY API KEY]'
        BASE_URL = 'https://cutt.ly/api/api.php'

        payload = {
            'key': API_KEY,
            'short': getLink,
            'name': ''
        }

        request = requests.get(BASE_URL, params=payload)
        data = request.json()

        title = data['url']['title']
        link = data['url']['shortLink']
        fullLink = data['url']['fullLink']

        update.callback_query.message.edit_text(f'Title : {title}\n\nLong link :- {fullLink}\n\nShorted link :- {link}\n\nLink type :- Cutt.ly')
    elif 'tinycom' in query:
        shortener = pyshorteners.Shortener()
        link = shortener.tinyurl.short(getLink)

        update.callback_query.message.edit_text(f'Long link :- {getLink}\n\nShorted link :- {link}\n\nLink type :- tinyurl.com')


def main():
    updater = Updater(API_KEY, use_context=True)
    dp = updater.dispatcher

    # Commands
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('help', help))
    dp.add_handler(CommandHandler('short', short))
    dp.add_handler(CallbackQueryHandler(queryHandler))

    # Run the bot
    updater.start_polling(1.0)
    updater.idle()

if __name__ == '__main__':
    main()
