import hdxpyutils
import requests

class NotifierManager:

    def __init__(self, NOTIFIER_BASE_URL: str):
        """NotifierManager Constructor.
        @param NOTIFIER_BASE_URL: NOTIFIER_BASE_URL.
        """
        self.NOTIFIER_BASE_URL = NOTIFIER_BASE_URL

    def send_email(self, subject: str, html: str, recipients: str, attachments=[]):
        """Send an email.
        
        @param subject: Email subject.
        @param html: Email body.
        @param recipients: Email recipients.         
        @param NOTIFIER_BASE_URL: NOTIFIER_BASE_URL.         
        @param attachments: Paths of the attached files.         
        """
        url = f'{self.NOTIFIER_BASE_URL}/api/v1/notify/email'
        data = {
            'subject': subject,
            'html': html,
            'cc': recipients,
        }

        s3m = hdxpyutils.S3Manager()
        S3_BUCKET = 'hdxetfsystems3files-corp'

        if attachments:
            data['attachments'] = [s3m.upload_file(S3_BUCKET, file) for file in attachments]

        response = requests.post(url, json=data)
        response.raise_for_status()
        print('Email enviado!')
        return True
    
    def send_slack_message(self, channel, message):
        """Send a message to a Slack channel."""

        url = f'{self.NOTIFIER_BASE_URL}/api/v1/notify/slack'
        data = {'channel': channel, 'message': message}
        response = requests.post(url, json=data)
        response.raise_for_status()
        return True