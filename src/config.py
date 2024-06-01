import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
PAYMENTS_API_TOKEN = os.getenv('PAYMENTS_API_TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')
DATABASE_URL = os.getenv('DATABASE_URL')
CHAT_OWNER_ID = int(os.getenv('CHAT_OWNER_ID'))
CVS_FILE_PATH = "subscriptions.cvs"
