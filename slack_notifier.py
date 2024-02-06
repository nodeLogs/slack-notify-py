from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

class SlackNotifier:
    def __init__(self, config):
        self.client = WebClient(token=config.slack_token)
        self.channel = config.slack_channel

    def send_message_with_buttons(self, message, buttons):
        try:
            blocks = [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": message
                    }
                },
                {
                    "type": "actions",
                    "elements": buttons
                }
            ]

            response = self.client.chat_postMessage(channel=self.channel, blocks=blocks)
            return response
        except SlackApiError as e:
            print(f"Error sending message: {e.response['error']}")
