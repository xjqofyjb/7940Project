import configparser
import logging
import app
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, CallbackContext, ConversationHandler
import os
from dotenv import load_dotenv

load_dotenv()

bot_token = os.getenv("TELEGRAM_ACCESS_TOKEN")

updater = Updater(token=bot_token, use_context=True)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

ADD_TITLE, ADD_COMMENT = range(2)

def gpt(update, context):
    reply_message = app.chatbot(update.message.text.upper())
    logging.info("Update: " + str(update))
    logging.info("context: " + str(context))
    context.bot.send_message(chat_id=update.effective_chat.id, text= reply_message)

def add(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Which movie do you want to review?")
    return ADD_TITLE

def add_title(update, context):
    logging.info("Update: " + str(update))
    logging.info("context: " + str(context))
    context.user_data['title'] = update.message.text
    context.bot.send_message(chat_id=update.effective_chat.id, text="Tell me about this movie.")
    return ADD_COMMENT

def add_comment(update, context):
    logging.info("Update: " + str(update))
    logging.info("context: " + str(context))
    title = context.user_data['title']
    content = update.message.text
    with open('docs/movie.txt', 'a') as file:
        file.write(f"\n{title}\n{content}\n\n###\n")
    context.bot.send_message(chat_id=update.effective_chat.id, text="Your review has been sent successfully.")
    return ConversationHandler.END

conv_handler = ConversationHandler(
    entry_points=[CommandHandler('add', add)],
    states={
        ADD_TITLE: [MessageHandler(Filters.text & ~Filters.command, add_title)],
        ADD_COMMENT: [MessageHandler(Filters.text & ~Filters.command, add_comment)],
    },
    fallbacks=[]
)

gpt_handler = MessageHandler(Filters.text & (~Filters.command), gpt)

dispatcher.add_handler(conv_handler)
dispatcher.add_handler(gpt_handler)

updater.start_polling()
updater.idle()