import smtplib
from dotenv import load_dotenv
import os
from telegram import Bot
from telegram.error import TelegramError


class NotificationManager:
    def __init__(self, telegram_token, telegram_chat_id, email_address=None, email_password=None):
        self.telegram_token = telegram_token
        self.telegram_chat_id = telegram_chat_id
        self.email_address = email_address
        self.email_password = email_password
        self.bot = Bot(token=self.telegram_token)

    # This method is responsible for sending notifications via Telegram
    async def send_telegram_message(self, message):
        try:
            await self.bot.send_message(chat_id=self.telegram_chat_id, text=message)
            print(f"Message sent successfully to {self.telegram_chat_id}")
        except TelegramError as e:
            print(f"Error sending message: {e}")

    # (Optional) This method is responsible for sending email notifications
    def send_email(self, subject, message, to_email):
        if not self.email_address or not self.email_password:
            raise ValueError("Email credentials not provided")

        try:
            with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
                connection.starttls()
                connection.login(user=self.email_address,
                                 password=self.email_password)
                msg = f"Subject:{subject}\n\n{message}".encode('utf-8')
                connection.sendmail(
                    from_addr=self.email_address,
                    to_addrs=to_email,
                    msg=msg
                )
            print(f"Email sent successfully to {to_email}")
        except Exception as e:
            print(f"Error sending email: {e}")
