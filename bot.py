
import os
import telebot
from telebot import types

BOT_TOKEN = os.getenv("BOT_TOKEN")
MINI_APP_URL = 'https://ha2u-bingo.pages.dev'
CHANNEL_USERNAME = '@Nana_Gamez'
CHANNEL_LINK = 'https://t.me/Nana_Gamez'

if not BOT_TOKEN:
    raise RuntimeError("Please set the BOT_TOKEN environment variable.")

bot = telebot.TeleBot(BOT_TOKEN)

# 1. User clicks /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True
    )
    btn_share = types.KeyboardButton(
        '📱 Share Contact to Continue',
        request_contact=True
    )
    markup.add(btn_share)

    bot.send_message(
        message.chat.id,
        "Welcome to Hahu Bingo! 🎉\n\nPlease share your phone number to unlock the game.",
        reply_markup=markup
    )

# 2. User shares contact
@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    user_id = message.from_user.id

    try:
        bot.add_chat_member(
            chat_id=CHANNEL_USERNAME,
            user_id=user_id
        )
        add_status = "✅ You have been automatically added to our channel!"
    except Exception as e:
        add_status = f"⚠️ We couldn't auto-add you. Please join manually: {CHANNEL_LINK}"
        print(f"Error adding user: {e}")

    remove_markup = types.ReplyKeyboardRemove()

    markup = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        row_width=2
    )
    btn_play = types.KeyboardButton('🎮 Play Hahu Bingo')
    btn_balance = types.KeyboardButton('💵 Balance')
    btn_invite = types.KeyboardButton('🔗 Invite')
    btn_support = types.KeyboardButton('🆘 Support')

    markup.add(btn_play, btn_balance)
    markup.add(btn_invite, btn_support)

    bot.send_message(
        message.chat.id,
        f"✅ Contact verified!\n\n{add_status}\n\nWelcome to the main menu:",
        reply_markup=markup
    )

# 3. User clicks Play
@bot.message_handler(func=lambda message: message.text == '🎮 Play Hahu Bingo')
def open_game(message):
    markup = types.InlineKeyboardMarkup()
    web_app_info = types.WebAppInfo(url=MINI_APP_URL)
    btn_open_app = types.InlineKeyboardButton(
        '🚀 Open Hahu Bingo',
        web_app=web_app_info
    )
    markup.add(btn_open_app)

    bot.send_message(
        message.chat.id,
        "Click below to launch the game:",
        reply_markup=markup
    )

# 4. Other buttons
@bot.message_handler(
    func=lambda message: message.text in [
        '💵 Balance', '🔗 Invite', '🆘 Support'
    ]
)
def handle_other_buttons(message):
    if message.text == '💵 Balance':
        bot.reply_to(message, "Your balance is: 0 ETB (Demo)")

    elif message.text == '🔗 Invite':
        bot.reply_to(
            message,
            "Share this link with friends: https://t.me/YOUR_BOT_USERNAME"
        )

    elif message.text == '🆘 Support':
        bot.reply_to(message, "Contact support: @YourSupportUsername")

print("Bot is running...")
bot.infinity_polling()
