import logging
import urllib

import os


class SMSHandler(logging.Handler):
    def emit(self, record):
        msg = urllib.parse.quote(self.format(record).encode('utf8'))
        try:
            urllib.request.urlopen("https://smsapi.free-mobile.fr/sendmsg?user=" +
                               os.environ.get("FREE_SMS_USER", "") + "&pass=" +
                               os.environ.get("FREE_SMS_PASS", "") + "&msg=" + msg)
        except urllib.error.HTTPError:
            pass
