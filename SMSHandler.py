import logging
import urllib

import config_sms

class SMSHandler(logging.Handler):
    def emit(self, record):
        msg = urllib.parse.quote(self.format(record).encode('utf8'))
        urllib.request.urlopen("https://smsapi.free-mobile.fr/sendmsg?user=" + config_sms.user + "&pass=" + config_sms.password + "&msg=" + msg)