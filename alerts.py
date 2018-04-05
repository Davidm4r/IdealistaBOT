import telebot
import configparser

config = configparser.ConfigParser()
config.read('config')

TOKEN =str(config['TELEGRAM']['Token'])
		
commands = {'start': 'Get your own code'}

def listener(messages):

    for m in messages:
        if m.content_type == 'text':
            print (str(m.chat.first_name) + " [" + str(m.chat.id) + "]: " +
                   m.text)

bot = telebot.TeleBot(TOKEN)
bot.set_update_listener(listener)

@bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id
    bot.send_message(cid,cid)

bot.polling()
