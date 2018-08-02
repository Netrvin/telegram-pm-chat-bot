#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import json
import telegram.ext
import telegram
import sys
import datetime
import os
import logging
import threading

reload(sys)
sys.setdefaultencoding('utf8')

Version_Code = 'v1.0.0'

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                    )

PATH = os.path.dirname(os.path.realpath(__file__)) + '/'

CONFIG = json.loads(open(PATH + 'config.json', 'r').read())

LANG = json.loads(open(PATH + 'lang/' + CONFIG['Lang'] + '.json').read())

MESSAGE_LOCK = False

message_list = json.loads(open(PATH + 'data.json', 'r').read())

PREFERENCE_LOCK = False

preference_list = json.loads(open(PATH + 'preference.json','r').read())

def save_data():
    global MESSAGE_LOCK
    while MESSAGE_LOCK:
        time.sleep(0.05)
    MESSAGE_LOCK = True
    f = open(PATH + 'data.json', 'w')
    f.write(json.dumps(message_list))
    f.close()
    MESSAGE_LOCK = False

def save_preference():
    global PREFERENCE_LOCK
    while PREFERENCE_LOCK:
        time.sleep(0.05)
    PREFERENCE_LOCK = True
    f = open(PATH + 'preference.json', 'w')
    f.write(json.dumps(preference_list))
    f.close()
    PREFERENCE_LOCK = False

def save_config():
    f = open(PATH + 'config.json', 'w')
    f.write(json.dumps(CONFIG, indent=4))
    f.close()

def init_user(user):
    global preference_list
    if not preference_list.has_key(str(user.id)):
        preference_list[str(user.id)]={}
        preference_list[str(user.id)]['notification']=True
        preference_list[str(user.id)]['name']=user.full_name
        threading.Thread(target=save_preference).start()
        return
    if preference_list[str(user.id)]['name']!=user.full_name:
        preference_list[str(user.id)]['name']=user.full_name
        threading.Thread(target=save_preference).start()

updater = telegram.ext.Updater(token=CONFIG['Token'])
dispatcher = updater.dispatcher

me = updater.bot.get_me()
CONFIG['ID'] = me.id
CONFIG['Username'] = '@' + me.username

print 'Starting... (ID: ' + str(CONFIG['ID']) + ', Username: ' + CONFIG['Username'] + ')'

def process_msg(bot, update):
    global message_list
    init_user(update.message.from_user)
    if CONFIG['Admin'] == 0:
        bot.send_message(chat_id=update.message.from_user.id,text=LANG['please_setup_first'])
        return
    if update.message.from_user.id == CONFIG['Admin']:
        if update.message.reply_to_message != None:
            if message_list.has_key(str(update.message.reply_to_message.message_id)):
                msg = update.message
                sender_id = message_list[str(update.message.reply_to_message.message_id)]['sender_id']
                try:
                    if msg.audio != None:
                        bot.send_audio(chat_id=sender_id,audio=msg.audio, caption=msg.caption)
                    elif msg.document != None:
                        bot.send_document(chat_id=sender_id,document=msg.document,caption=msg.caption)
                    elif msg.voice != None:
                        bot.send_voice(chat_id=sender_id,voice=msg.voice, caption=msg.caption)
                    elif msg.video != None:
                        bot.send_video(chat_id=sender_id,video=msg.video, caption=msg.caption)
                    elif msg.sticker != None:
                        bot.send_sticker(chat_id=sender_id, sticker=update.message.sticker)
                    elif msg.photo:
                        bot.send_photo(chat_id=sender_id,photo=msg.photo[0], caption=msg.caption)
                    elif msg.text_markdown != None:
                        bot.send_message(chat_id=sender_id,text=msg.text_markdown,parse_mode=telegram.ParseMode.MARKDOWN)
                    else:
                        bot.send_message(chat_id=CONFIG['Admin'],text=LANG['reply_type_not_supported'])
                        return
                except Exception as e:
                    if e.message == "Forbidden: bot was blocked by the user":
                        bot.send_message(chat_id=CONFIG['Admin'],text=LANG['blocked_alert'])
                    else:
                        bot.send_message(chat_id=CONFIG['Admin'],text=LANG['reply_message_failed'])
                    return
                if preference_list[str(update.message.from_user.id)]['notification']:
                    bot.send_message(chat_id=update.message.chat_id,text=LANG['reply_message_sent'] % (preference_list[str(sender_id)]['name'],str(sender_id)),parse_mode=telegram.ParseMode.MARKDOWN)
            else:
                bot.send_message(chat_id=CONFIG['Admin'],text=LANG['reply_to_message_no_data'])
        else:
            bot.send_message(chat_id=CONFIG['Admin'],text=LANG['reply_to_no_message'])
    else:
        fwd_msg = bot.forward_message(chat_id=CONFIG['Admin'], from_chat_id=update.message.chat_id, message_id=update.message.message_id)
        if preference_list[str(update.message.from_user.id)]['notification']:
            bot.send_message(chat_id=update.message.from_user.id,text=LANG['message_received_notification'])
        message_list[str(fwd_msg.message_id)]={}
        message_list[str(fwd_msg.message_id)]['sender_id']=update.message.from_user.id
        threading.Thread(target=save_data).start()
    pass


def process_command(bot, update):
    init_user(update.message.from_user)
    id=update.message.from_user.id
    global CONFIG
    command = update.message.text[1:].replace(CONFIG['Username'], '').lower().split()
    if command[0] == 'start':
        bot.send_message(chat_id=update.message.chat_id,
                         text=LANG['start'])
        return
    elif command[0] == 'version':
        bot.send_message(chat_id=update.message.chat_id,
                         text='Telegram Private Message Chat Bot\n'
                         + Version_Code
                         + '\nhttps://github.com/Netrvin/telegram-pm-chat-bot'
                         )
        return
    elif command[0] == 'setadmin':
        if CONFIG['Admin']==0:
            CONFIG['Admin']=int(update.message.from_user.id)
            save_config()
            bot.send_message(chat_id=update.message.chat_id,text=LANG['set_admin_successful'])
        else:
            bot.send_message(chat_id=update.message.chat_id,text=LANG['set_admin_failed'])
        return
    elif command[0] == 'togglenotification':
        global preference_list
        preference_list[str(id)]['notification']=(preference_list[str(id)]['notification'] == False)
        threading.Thread(target=save_preference).start()
        if preference_list[str(id)]['notification']:
            bot.send_message(chat_id=update.message.chat_id,text=LANG['togglenotification_on'])
        else:
            bot.send_message(chat_id=update.message.chat_id,text=LANG['togglenotification_off'])
    elif command[0] == 'info':
        if (update.message.from_user.id == CONFIG['Admin']) and (update.message.chat_id == CONFIG['Admin']):
            if update.message.reply_to_message != None:
                if message_list.has_key(str(update.message.reply_to_message.message_id)):
                    sender_id=message_list[str(update.message.reply_to_message.message_id)]['sender_id']
                    bot.send_message(chat_id=update.message.chat_id,text=LANG['info_data'] % (preference_list[str(sender_id)]['name'],str(sender_id)),parse_mode=telegram.ParseMode.MARKDOWN)
                else:
                    bot.send_message(chat_id=update.message.chat_id,text=LANG['reply_to_message_no_data'])

dispatcher.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.all & telegram.ext.Filters.private & (~ telegram.ext.Filters.command) & (~ telegram.ext.Filters.status_update), process_msg))

dispatcher.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.command & telegram.ext.Filters.private,
                                                   process_command))

updater.start_polling()
print 'Started'
updater.idle()
print 'Stopping...'
save_data()
save_preference()
print 'Data saved.'
print 'Stopped.'
