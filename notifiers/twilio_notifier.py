"""Notifier that sends messages through Twilio"""

import logging

from notifiers.base_notifier import Notifier
from twilio.rest import Client

_logger = logging.getLogger(__name__)


class TwilioNotifier(Notifier):
    """Notifier class to work with twilio"""

    def __init__(self, config):
        """Override init to check settings"""
        self.twilio_account_sid = config[
            "twilio_account_sid"
        ]
        self.twilio_auth_token = config["twilio_auth_token"]
        self.twilio_recipient = config["twilio_recipient"]
        self.twilio_sender = config["twilio_sender"]

        super(TwilioNotifier, self).__init__(config)

    def check_requirements(self):
        """Log in to Twilio and check credentials and settings"""
        client = Client(
            self.twilio_account_sid, self.twilio_auth_token
        )

        try:
            account = client.api.accounts(
                self.twilio_account_sid
            ).fetch()
        except Exception as ex:
            _logger.error(
                "Cannot connect to your Twilio account. "
                "Correct your config and try again. Error details:"
            )
            _logger.error(ex)
            raise
        _logger.info(
            "Twilio account: {}, status: {}".format(
                account.friendly_name, account.status
            )
        )

    def notify(self, title, text, url=False):
        """Send sms notification using twilio"""
        body = text + " - " + url
        client = Client(
            self.twilio_account_sid, self.twilio_auth_token
        )
        message = client.messages.create(
            from_=self.twilio_sender,
            body=body,
            to=self.twilio_recipient,
        )
        _logger.debug(
            "SMS sent, twilio response: {}".format(
                message.sid
            )
        )
