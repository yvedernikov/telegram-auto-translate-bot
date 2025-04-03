from telegram.ext import Updater, MessageHandler, Filters
from googletrans import Translator
from telegram import constants
import re
import config
import time


translator = Translator()

def escape_markdown(text):
    escape_chars = r'_*[]()~`>#+-=|{}.!'
    return re.sub(f'([{re.escape(escape_chars)}])', r'\\\1', text)

def translate_message(update, context):

    if update.channel_post:  # For channels
        message = update.channel_post
    elif update.message:  # For groups (if added)
        message = update.message
    else:
        return

    try:
        message_text = message.text
        if len(message_text) > 4096:
            # Telegram's message length limit
            message_text = message_text[:4000] + "..."

        print(f"Original message: {message_text}")
        print(f"Escaped message: {escape_markdown(message_text)}")
        translated = translator.translate(escape_markdown(message_text), dest=config.TARGET_LANG).text
        # context.bot.send_message(
        #     chat_id=update.effective_chat.id,
        #     text=f"🌍 Translated to {config.TARGET_LANG}:\n{translated}"
        # )

        print(f"Translated message: {translated}")
        context.bot.edit_message_text(
            text=escape_markdown(translated),
            chat_id=update.effective_chat.id,
            message_id=message.message_id,
            parse_mode='MarkdownV2'
        )

        time.sleep(0.3)
    except Exception as e:
        print(f"Error: {e}")

updater = Updater(config.BOT_TOKEN, use_context=True)
updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, translate_message))

print("Bot started! Press Ctrl+C to stop.")
updater.start_polling()
updater.idle()
