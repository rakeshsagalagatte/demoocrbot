#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""


from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
# try:
#     from PIL import Image
# except ImportError:
#     import Image
# import pytesseract
from traceback import print_exc
import cloudmersive_ocr_api_client
from cloudmersive_ocr_api_client.rest import ApiException
import json
import os



CLOUDMERSIVE_API_KEY = os.environ.get("CLOUDMERSIVE_API_KEY","")

# Configure API key authorization: Apikey
configuration = cloudmersive_ocr_api_client.Configuration()
configuration.api_key['Apikey'] = CLOUDMERSIVE_API_KEY



def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update, context):
    """Echo the user message."""
    query = update.message.text
    update.message.reply_text("I got query : " + query)

def donate(update, context):
    update.message.reply_text("Thanks for hitting donate command!")

def convert_image(update , context):
    print(update.message)
    filename = "test.jpg"
    file_id = update.message.photo[-1].file_id
    newFile = context.bot.get_file(file_id)
    print(update.message.photo)
    newFile.download(filename)

    update.message.reply_text("I got image :)")
    # Simple image to string
    # try:
    #     #pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'
    #     extrated_string = pytesseract.image_to_string(Image.open(filename))
    # except Exception:
    #     print_exc()

    ''' CLOUDMERSIVE  cloud code  '''

    # try:
    #     # Recognize a photo of a receipt, extract key business information
    #     api_response = api_instance.image_ocr_photo_recognize_receipt(image_file, recognition_mode=recognition_mode, language=language, preprocessing=preprocessing)
    #     print(api_response)
    # except ApiException as e:
    #     print("Exception when calling ImageOcrApi->image_ocr_photo_recognize_receipt: %s\n" % e)

    ''' Cyberboy code for API '''

    api_instance = cloudmersive_ocr_api_client.ImageOcrApi()
    api_instance.api_client.configuration.api_key = {}
    api_instance.api_client.configuration.api_key['Apikey'] = CLOUDMERSIVE_API_KEY
    try:
        api_response = api_instance.image_ocr_post(filename)
        print(api_response)
        confidence = api_response.mean_confidence_level
        update.message.reply_text("Confidence: " + str(confidence)+"\nExtracted text is : " + api_response.text_result)
    except ApiException:
        print_exc() 

    # if extrated_string is not None:
    #     update.message.reply_text(extrated_string)
    # else:
    #     update.message.reply_text("Sorry I can't able to extract text from image!:(")
    
    

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    bot_token = os.environ.get("BOT_TOKEN","")
    updater = Updater(bot_token, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("donate", donate))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))
    dp.add_handler(MessageHandler(Filters.photo, convert_image))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
