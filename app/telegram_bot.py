import logging
import time
from functools import wraps
from typing import Optional

import telegram
from app.helper import retry
from app.logger import RichHandler
from app.config import settings_dev

logging.basicConfig(
    level="INFO", format="%(message)s", datefmt="[%x %X]", handlers=[RichHandler()]
)
logger = logging.getLogger(__name__)


class TelegramBot:
    def __init__(
        self,
        token: str = settings_dev.TELEGRAM_TOKEN,
        chat_id: str = settings_dev.TELEGRAM_CHAT_ID,
        parse_mode: bool = True,
        spider_name: str = "Unknown",
    ):
        self.token = token
        self.chat_id = chat_id
        self.bot = telegram.Bot(token=self.token)
        self.parse_mode = telegram.ParseMode.MARKDOWN if parse_mode else None
        self.spider_name = spider_name

    @retry(retry_times=10, interval=5)
    def send_bot_msg(
        self,
        content_msg: str,
        reply_to_msg_id: Optional[str] = None,
        markup_url: str = None,
        markup_text: str = "Open Direct Link",
        chat_id: int = None,
        disable_web_page_preview: bool = None,
        disable_notification: bool = None,
    ) -> telegram.Message:
        """Given a string msg and msg_id, send msg to telegram chat_id.

        Args:
            content_msg (str): The string msg to send to telegram.
            reply_to_msg_id (str or None, optional): The msg_id to be quoted when sending msg. Defaults to None.

        Returns:
            telegram.Message: Return a Message object sent successfully
        """
        if not chat_id:
            # If no chat_id, then use the default chat_id
            chat_id = self.chat_id

        log_content = content_msg.replace("\n", " ")
        logger.info(f"## {self.spider_name} Sending: {log_content}")

        if markup_url:
            keyboard = [
                [
                    telegram.InlineKeyboardButton(markup_text, url=markup_url),
                ],
            ]
            reply_markup = telegram.InlineKeyboardMarkup(keyboard)
        else:
            reply_markup = None

        try:
            returned_msg = self.bot.send_message(
                text=content_msg,
                chat_id=chat_id,
                reply_to_message_id=reply_to_msg_id,
                reply_markup=reply_markup,
                parse_mode=self.parse_mode,
                disable_web_page_preview=disable_web_page_preview,
                disable_notification=disable_notification,
            )
            sent_log_msg = (
                f'{self.spider_name} succeeds to send msg. [tg_msg_id]: {returned_msg["message_id"]} '
                + f'[Disable Notification]: {"✔️" if disable_notification else "❌"} '
                + f'[Disable Web View]: {"✔️" if disable_web_page_preview else "❌"}'
            )

            logger.info(sent_log_msg)
            time.sleep(3)

            return returned_msg
        except Exception as e:
            error_msg = (
                f"## {self.spider_name} failed to send msg {content_msg}\n## Error: {e}"
            )
            logger.error(error_msg)

            raise Exception(e)

    @retry(retry_times=3, interval=5)
    def pin_message(self, pin_message_id: int) -> bool:
        """Pin a telegram message with a pin_message_id.

        Args:
            pin_message_id (int): The message id to be pinned

        Returns:
            bool: Return True if the message is pinned successfully
        """
        return self.bot.pin_chat_message(
            chat_id=self.chat_id, message_id=pin_message_id
        )

    @retry(retry_times=2, interval=15)
    def edit_message(
        self,
        content_msg: str,
        edit_msg_id: str = None,
        markup_url: str = None,
        markup_text: str = "Open Direct Link",
        chat_id: int = None,
        disable_web_page_preview: bool = None,
    ) -> telegram.Message:
        """Given a string msg and msg_id, update the sent msg in chat_id.

        Args:
            content_msg (str): The string msg to send to telegram.
            edit_msg_id (str or None): The msg_id to be updated.

        Returns:
            telegram.Message: Return a Message object updated successfully
        """
        if not chat_id:
            # If no chat_id, then use the default chat_id
            chat_id = self.chat_id

        if markup_url:
            keyboard = [
                [
                    telegram.InlineKeyboardButton(markup_text, url=markup_url),
                ],
            ]
            reply_markup = telegram.InlineKeyboardMarkup(keyboard)
        else:
            reply_markup = None

        # Try to send message to the telegram chat
        returned_msg = self.bot.edit_message_text(
            text=content_msg,
            chat_id=chat_id,
            message_id=edit_msg_id,
            reply_markup=reply_markup,
            parse_mode=self.parse_mode,
            disable_web_page_preview=disable_web_page_preview,
        )

        # logger.info('## Msg was edited successfully!')
        time.sleep(3)

        if returned_msg:
            return returned_msg
        else:
            logger.error(
                f"## {self.spider_name} failed to update msg {content_msg}\n## Error: {e}"
            )

            return None

    def send_photo(
        self,
        photo: str,
        chat_id: int = None,
        caption: str = None,
        reply_to_message_id: int = None,
        disable_notification: bool = None,
    ) -> telegram.Message:
        if not chat_id:
            # If no chat_id, then use the default chat_id
            chat_id = self.chat_id

        try:
            returned_msg = self.bot.send_photo(
                chat_id=chat_id,
                photo=photo,
                parse_mode=self.parse_mode,
                caption=caption,
                reply_to_message_id=reply_to_message_id,
                disable_notification=disable_notification,
            )

            # logger.info('## Msg was edited successfully!')
            time.sleep(3)

            return returned_msg
        except Exception as e:
            logger.error(
                f"## {self.spider_name} failed to send photo {photo}\n## Error:\n{e}"
            )

            raise Exception(e)
