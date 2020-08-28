# -*- coding: utf-8 -*-
import requests
import json
import configparser as cfg
import urllib

class telegram_bot():

    def __init__(self, config):
        self.token = self.read_token_from_config_file(config)
        self.base = "https://api.telegram.org/bot{}/".format(self.token)

    def get_updates(self, offset=None):
        url = self.base + "getUpdates?timeout=100"
        if offset:
            url = url + "&offset={}".format(offset + 1)
        r = requests.get(url)
        return json.loads(r.content)

    def build_keyboard(self, items):
        keyboard = [[item] for item in items]
        reply_markup = {"keyboard":keyboard, "one_time_keyboard": True}
        return json.dumps(reply_markup)

    def send_message(self, msg, chat_id, msg_id, reply_markup=None):
        if msg is not None:
            msg = urllib.parse.quote_plus(msg)
            url = self.base + "sendMessage?chat_id={}&reply_to_message_id={}&text={}".format(chat_id, msg_id, msg)
            if reply_markup:
                url += "&reply_markup={}".format(reply_markup)
            requests.get(url)

    def read_token_from_config_file(self, config):
        parser = cfg.ConfigParser()
        parser.read(config)
        return parser.get('creds', 'token')

    