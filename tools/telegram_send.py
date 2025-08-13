import requests
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv('telegram_token')
chat_id = os.getenv('telegram_chat_id')

def sendMessage(message : str) -> None:
    """Send a message to a Telegram chat using the Telegram Bot API."""

    if not message:
        raise ValueError("Message cannot be empty.")
    if not token:
        raise ValueError("Telegram token is not set in the environment variables.")

    url = f'https://api.telegram.org/bot{token}/sendMessage'
    data = {
        'chat_id': chat_id, 
        'text': message,
        'parse_mode': "html",
        'disable_web_page_preview': False,
        'disable_notification': False
    }
    response = requests.post(url, data=data)
    print(response.text)
    if response.status_code != 200:
        raise Exception(f"Failed to send message: {response.text}")
    