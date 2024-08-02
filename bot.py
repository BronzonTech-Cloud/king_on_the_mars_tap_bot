import sqlite3
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from database import create_db, get_user, update_taps, set_user_address
from ton import is_valid_ton_address, send_ton_tokens

TELEGRAM_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

def start(update, context):
    user_id = update.message.from_user.id
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('INSERT OR IGNORE INTO users (user_id, taps) VALUES (?, 0)', (user_id,))
    conn.commit()
    conn.close()
    update.message.reply_text('Welcome to KingOnTheMars Tap Bot! Send me your TON address with /setaddress command.')

def set_address(update, context):
    user_id = update.message.from_user.id
    if len(context.args) == 0:
        update.message.reply_text('Please provide your TON address.')
        return
    
    address = context.args[0]
    if is_valid_ton_address(address):
        set_user_address(user_id, address)
        update.message.reply_text('Your TON address has been set.')
    else:
        update.message.reply_text('Invalid TON address.')

def tap(update, context):
    user_id = update.message.from_user.id
    update_taps(user_id)
    taps = get_user(user_id)['taps']
    update.message.reply_text(f'You tapped! Total taps: {taps}')

def main():
    create_db()
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("setaddress", set_address, pass_args=True))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, tap))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
