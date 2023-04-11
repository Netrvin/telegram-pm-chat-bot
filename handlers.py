import threading

from telegram import Update, ParseMode
from telegram.ext import CallbackContext, Filters, MessageHandler

from settings import init_user, message_list, preference_list, save_config, save_data, save_preference, \
    CONFIG, LANG, VERSION


# process message
def process_msg(update: Update, context: CallbackContext):
    init_user(update.effective_user)
    id = update.effective_user.id
    msg = update.effective_message
    fwd_msg = context.bot.forward_message(chat_id=CONFIG['admin'],
                                          from_chat_id=msg.chat_id,
                                          message_id=msg.message_id)

    # if not admin
    if CONFIG['admin'] == 0:
        context.bot.send_message(chat_id=id, text=LANG['please_setup_first'])
        return

    # if message sent by admin
    if msg.from_user.id == CONFIG['admin']:
        if msg.reply_to_message:
            if str(msg.reply_to_message.message_id) in message_list:
                sender_id = message_list[str(msg.reply_to_message.message_id)]['sender_id']
                msg_type_handlers = {
                    'audio': context.bot.send_audio,
                    'document': context.bot.send_document,
                    'voice': context.bot.send_voice,
                    'video': context.bot.send_video,
                    'sticker': context.bot.send_sticker,
                    'photo': context.bot.send_photo,
                    'text_markdown': lambda chat_id, text: context.bot.send_message(chat_id=chat_id, text=text,
                                                                                    parse_mode=ParseMode.MARKDOWN)
                }

                msg_type = next((key for key in msg_type_handlers.keys() if getattr(msg, key, None)), None)

                if not msg_type:
                    context.bot.send_message(chat_id=CONFIG['admin'], text=LANG['reply_type_not_supported'])
                    return

                # anonymous forwarding
                try:
                    msg_type_handlers[msg_type](chat_id=sender_id,
                                                **{msg_type: getattr(msg, msg_type), 'caption': msg.caption})

                except Exception as e:
                    if 'Forbidden: bot was blocked by the user' in str(e):
                        context.bot.send_message(chat_id=CONFIG['admin'],
                                                 text=LANG['blocked_alert'])
                    else:
                        context.bot.send_message(chat_id=CONFIG['admin'],
                                                 text=LANG['reply_message_failed'])
                    return

                if preference_list[str(id)]['notification']:  # if notification is enabled
                    context.bot.send_message(chat_id=msg.chat_id,
                                             text=LANG['reply_message_sent'] % (preference_list[str(sender_id)]['name'],
                                                                                str(sender_id)),
                                             parse_mode=ParseMode.MARKDOWN)

            else:
                context.bot.send_message(chat_id=CONFIG['admin'],
                                         text=LANG['reply_to_message_no_data'])

        else:
            context.bot.send_message(chat_id=CONFIG['admin'],
                                     text=LANG['reply_to_no_message'])

    else:  # if message sent by user
        if preference_list[str(id)]['blocked']:
            context.bot.send_message(chat_id=id,
                                     text=LANG['be_blocked_alert'])
            return

        if fwd_msg.sticker:  # if forward message is sticker, send sender identity
            context.bot.send_message(chat_id=CONFIG['admin'],
                                     text=LANG['info_data'] % (update.effective_user.full_name,
                                                               str(id)),
                                     parse_mode=ParseMode.MARKDOWN,
                                     reply_to_message_id=fwd_msg.message_id)

        if preference_list[str(id)]['notification']:  # if notification is enabled, send notification
            context.bot.send_message(chat_id=id,
                                     text=LANG['message_received_notification'])

        message_list[str(fwd_msg.message_id)] = {}
        message_list[str(fwd_msg.message_id)]['sender_id'] = id
        threading.Thread(target=save_data).start()  # save data in a new thread


# process command
def process_command(update: Update, context: CallbackContext):
    init_user(update.effective_user)
    id = update.effective_user.id
    msg = update.effective_message
    command = msg.text[1:].replace(CONFIG['username'], '').lower().split()

    if command[0] == 'start':
        context.bot.send_message(chat_id=msg.chat_id, text=LANG['start'])

    elif command[0] == 'help':
        context.bot.send_message(chat_id=msg.chat_id,
                                 text='Telegram Private Message Chat Bot\n'
                                      + VERSION
                                      + '\nhttps://github.com/Netrvin/telegram-pm-chat-bot'
                                 )

    elif command[0] == 'setadmin':  # set admin
        if CONFIG['admin'] == 0:
            CONFIG['admin'] = int(id)
            save_config()
            context.bot.send_message(chat_id=msg.chat_id, text=LANG['set_admin_successful'])
        else:
            context.bot.send_message(chat_id=msg.chat_id, text=LANG['set_admin_failed'])
        return

    elif command[0] == 'notification':  # toggle notification
        preference_list[str(id)]['notification'] = not preference_list[str(id)]['notification']
        threading.Thread(target=save_preference).start()

        if preference_list[str(id)]['notification']:
            context.bot.send_message(chat_id=msg.chat_id, text=LANG['notification_on'])
        else:
            context.bot.send_message(chat_id=msg.chat_id, text=LANG['notification_off'])

    elif command[0] == 'info':  # show sender info
        if id == CONFIG['admin'] and msg.chat_id == CONFIG['admin']:
            if msg.reply_to_message:
                if str(msg.reply_to_message.message_id) in message_list:
                    sender_id = message_list[str(msg.reply_to_message.message_id)]['sender_id']
                    context.bot.send_message(chat_id=msg.chat_id,
                                             text=LANG['info_data'] % (preference_list[str(sender_id)]['name'],
                                                                       str(sender_id)),
                                             parse_mode=ParseMode.MARKDOWN,
                                             reply_to_message_id=msg.reply_to_message.message_id)
                else:
                    context.bot.send_message(chat_id=msg.chat_id,
                                             text=LANG['reply_to_message_no_data'])
            else:
                context.bot.send_message(chat_id=msg.chat_id,
                                         ext=LANG['reply_to_no_message'])
        else:
            context.bot.send_message(chat_id=msg.chat_id,
                                     text=LANG['not_an_admin'])

    elif command[0] == 'ping':  # Ping~Pong!
        context.bot.send_message(chat_id=msg.chat_id, text='Pong!')

    elif command[0] == 'ban':  # ban user
        if id == CONFIG['admin'] and msg.chat_id == CONFIG['admin']:
            if msg.reply_to_message:
                if str(msg.reply_to_message.message_id) in message_list:
                    sender_id = message_list[str(msg.reply_to_message.message_id)]['sender_id']
                    preference_list[str(sender_id)]['blocked'] = True
                    context.bot.send_message(chat_id=msg.chat_id,
                                             text=LANG['ban_user'] % (preference_list[str(sender_id)]['name'],
                                                                      str(sender_id)),
                                             parse_mode=ParseMode.MARKDOWN)
                    context.bot.send_message(chat_id=sender_id, text=LANG['be_blocked_alert'])
                else:
                    context.bot.send_message(chat_id=msg.chat_id, text=LANG['reply_to_message_no_data'])
            else:
                context.bot.send_message(chat_id=msg.chat_id, text=LANG['reply_to_no_message'])
        else:
            context.bot.send_message(chat_id=msg.chat_id, text=LANG['not_an_admin'])

    elif command[0] == 'unban':  # unban user
        if id == CONFIG['admin'] and msg.chat_id == CONFIG['admin']:
            if msg.reply_to_message:
                if str(msg.reply_to_message.message_id) in message_list:
                    sender_id = message_list[str(msg.reply_to_message.message_id)]['sender_id']
                    preference_list[str(sender_id)]['blocked'] = False
                    context.bot.send_message(chat_id=msg.chat_id,
                                             text=LANG['unban_user']
                                                  % (preference_list[str(sender_id)]['name'],
                                                     str(sender_id)),
                                             parse_mode=ParseMode.MARKDOWN)
                    context.bot.send_message(chat_id=sender_id, text=LANG['be_unbanned'])
                else:
                    context.bot.send_message(chat_id=msg.chat_id, text=LANG['reply_to_message_no_data'])
            elif len(command) == 2:
                if command[1] in preference_list:
                    preference_list[command[1]]['blocked'] = False
                    context.bot.send_message(chat_id=msg.chat_id,
                                             text=LANG['unban_user'] % (preference_list[command[1]]['name'],
                                                                        command[1]),
                                             parse_mode=ParseMode.MARKDOWN)
                    context.bot.send_message(chat_id=int(command[1]), text=LANG['be_unbanned'])
                else:
                    context.bot.send_message(chat_id=msg.chat_id, text=LANG['user_not_found'])
            else:
                context.bot.send_message(chat_id=msg.chat_id, text=LANG['reply_or_enter_id'])
        else:
            context.bot.send_message(chat_id=msg.chat_id, text=LANG['not_an_admin'])

    else:
        context.bot.send_message(chat_id=msg.chat_id, text=LANG['nonexistent_command'])


# add handlers
def setup_dispatcher(dp):
    dp.add_handler(MessageHandler(Filters.all
                                  & Filters.chat_type.private
                                  & ~Filters.command
                                  & ~Filters.status_update,
                                  process_msg))

    dp.add_handler(MessageHandler(Filters.command
                                  & Filters.chat_type.private,
                                  process_command))
