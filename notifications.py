import smtplib
from dotenv import load_dotenv
import os
from telegram import Bot
from telegram.error import TelegramError

load_dotenv()


TGRAM_BOT_TOKEN = os.getenv('flight_deal_finder_bot_token')
TGRAM_BOT_USERNAME = os.getenv('flight_deal_finder_bot_user_name')
CHAT_ID = os.getenv('flight_deal_finder_bot_chat_id')

my_email = os.getenv("my_email")
password = os.getenv("password")


def send_email(subject, message, to_email, user_email=my_email, user_password=password, email_provider="smtp.gmail.com"):
    """email_provider: Gmail (smtp.gmail.com), Yahoo (smtp.mail.yahoo.com), 
    Hotmail (smtp.live.com), Outlook (smtp-mail.outlook.com)"""
    with smtplib.SMTP(email_provider) as connection:  # gmail smtp server
        connection.starttls()  # for encryption
        try:
            connection.login(user=user_email, password=user_password)
            msg = f"Subject:{subject}\n\n{message}".encode('utf-8')
            connection.sendmail(from_addr=user_email,
                                to_addrs=to_email,
                                msg=msg)
            print(f"Message Sent to {to_email}!")
        except Exception as e:
            print(f"Error! Message not sent: {e}")


async def send_telegram_message(message):
    try:
        bot = Bot(token=TGRAM_BOT_TOKEN)
        await bot.send_message(chat_id=CHAT_ID, text=message)
        print(f"Message sent successfully to {TGRAM_BOT_USERNAME}")
    except TelegramError as e:
        print(f"Error sending message: {e}")


# use this to get chat id:
# create bot freshly,
# get the token, username etc.,
# search bot by both name,
# send a /start message to initiate the conversation
# Run the below line to get the chat id
# url = f"https://api.telegram.org/bot{TGRAM_BOT_TOKEN}/getUpdates"
# print(requests.get(url).json())
