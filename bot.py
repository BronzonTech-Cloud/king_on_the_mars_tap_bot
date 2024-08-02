import sqlite3
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from database import create_db, get_user, update_taps, set_user_address, set_last_claimed
from ton import is_valid_ton_address, send_ton_tokens
from datetime import datetime, timedelta

TELEGRAM_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

# Daily reward amount
DAILY_REWARD_AMOUNT = 10

def start(update, context):
    user_id = update.message.from_user.id
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('INSERT OR IGNORE INTO users (user_id, taps) VALUES (?, 0)', (user_id,))
    conn.commit()
    conn.close()
    update.message.reply_text('Welcome to KingOnTheMars Tap Bot! Send me your TON address with /setaddress command or check your rewards with /reward command.')

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

def reward(update, context):
    user_id = update.message.from_user.id
    user = get_user(user_id)
    if not user['address']:
        update.message.reply_text('Please set your TON address with /setaddress first.')
        return

    last_claimed = user.get('last_claimed')
    if last_claimed:
        last_claimed = datetime.strptime(last_claimed, '%Y-%m-%d %H:%M:%S')
    else:
        last_claimed = datetime.min

    if datetime.now() - last_claimed < timedelta(days=1):
        update.message.reply_text('You have already claimed your daily reward today. Please try again tomorrow.')
        return

    send_ton_tokens(user['address'], DAILY_REWARD_AMOUNT)
    set_last_claimed(user_id, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    update.message.reply_text(f'You have claimed your daily reward of {DAILY_REWARD_AMOUNT} TON tokens!')

def main():
    create_db()
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("setaddress", set_address, pass_args=True))
    dp.add_handler(CommandHandler("reward", reward))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, tap))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()