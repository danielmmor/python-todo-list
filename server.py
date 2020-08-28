# -*- coding: utf-8 -*-
from tele_bot import telegram_bot
#from donchian import pesquisa
from dbhelper import DBHelper

db = DBHelper()
db.setup()

bot = telegram_bot("config.cfg")

update_id = None
while True:
    updates = bot.get_updates(offset=update_id)
    updates = updates['result']
    if updates:
        for item in updates:
            update_id = item['update_id']
            text = item["message"]["text"]
            reply_to = str(item['message']['message_id'])
            from_ = item['message']['chat']['id']
            # parte do SQL
            items = db.get_items(from_)
            if text == "/done":
                keyboard = bot.build_keyboard(items)
                bot.send_message("Select an item to delete", from_, reply_to, keyboard)
            elif text == "/start":
                bot.send_message("Welcome to your personal To Do list. Send any text to me and I'll store it as an item. Send /done to remove items", from_, reply_to)
            elif text.startswith("/"):
                continue
            elif text in items:
                db.delete_item(text, from_)
                items = db.get_items(from_)
                itemsList = "\n".join(items)
                reply = "Item [{}] removido com sucesso!\nItens na lista:\n{}".format(text, itemsList)
                bot.send_message(reply, from_, reply_to)
            else:
                db.add_item(text, from_)
                items = db.get_items(from_)
                reply = "\n".join(items)
                try:
                    #reply = pesquisa(message)
                    bot.send_message(reply, from_, reply_to)
                    print(reply)
                except:
                    deu_ruim = None
