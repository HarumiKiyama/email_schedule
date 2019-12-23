import requests
import hashlib
import hmac

from app.exceptions import MailGunCallException


class Mailgunext:
    def __init__(self, ns='EMAIL_'):
        self.ns = ns

    def init_app(self, app):
        opts = app.config.get_namespace(self.ns)
        self.send_api = 'https://api.mailgun.net/v3/{}/messages'.format(
            opts['domain_name'])
        self.sender = opts['sender']
        self.api_key = opts['api_key']

    def send_email(self, to, subject, body):
        rv = requests.post(self.send_api,
                           auth=('api', self.api_key),
                           data={
                               'from':
                               '{}@{}'.format(self.sender, self.domain_name),
                               'to':
                               to,
                               'subject':
                               subject,
                               'text':
                               body,
                               'o:tracking':
                               True,
                           })
        if rv.status_code != 200:
            raise MailGunCallException(
                'call mailgun error, status_code: {}, response content: {}'.
                format(rv.status_code, rv.content))
        return rv.json()

    def verify(self, token, timestamp, signature):
        hmac_digest = hmac.new(key=self.api_key.encode(),
                               msg='{}{}'.format(timestamp, token).encode(),
                               digestmod=hashlib.sha256).hexdigest()
        return hmac.compare_digest(str(signature), str(hmac_digest))
