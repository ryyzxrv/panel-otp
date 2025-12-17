import os
import json
import time
import html
import requests
from telebot import TeleBot, types

# ===== CONFIG =====
BOT_TOKEN = "8341224653:AAEGPHzPlmxujlXFZhfW3Yi61FyIbb_n-bQ"
ADMIN_IDS = [7562165596]
DATA_FILE = "data.json"

# Masukkan Token API DGROUP Anda di sini
API_TOKEN = "Q05YRzRSQn6DiHh6SHdzX4hSjV9yU4ZKeVaOemCDUYB0ZpKAZpZt"
API_URL = "http://51.77.216.195/crapi/dgroup/viewstats"

GROUP_LINK = "https://t.me/EdogawaOTP"
CHANNEL_LINK = "https://t.me/proof_rvn"

# ===== Initialize Bot =====
bot = TeleBot(BOT_TOKEN)

# ===== Global Data =====
country_numbers = {}
user_numbers = {}
used_numbers_global = {}
user_languages = {}

# ===== Languages =====
LANG = {
    'en': {
        'start': "【 𝗜𝗟𝗬 𝗢𝗧𝗣 𝗕𝗢𝗧 】\n\n→ 𝗦𝗲𝗹𝗲𝗰𝘁 𝗮𝗻 𝗼𝗽𝘁𝗶𝗼𝗻 𝗳𝗿𝗼𝗺 𝘁𝗵𝗲 𝗺𝗲𝗻𝘂 𝗯𝗲𝗹𝗼𝘄 👇",
        'upload_btn': '📤 𝗨𝗽𝗹𝗼𝗮𝗱 𝗡𝘂𝗺𝗯𝗲𝗿𝘀',
        'status_btn': '📊 𝗣𝗮𝗻𝗲𝗹 𝗦𝘁𝗮𝘁𝘂𝘀',
        'reset_btn': '♻️ 𝗥𝗲𝘀𝗲𝘁 𝗔𝗹𝗹 𝗗𝗮𝘁𝗮',
        'del_country_btn': '🗑 𝗗𝗲𝗹𝗲𝘁𝗲 𝗖𝗼𝘂𝗻𝘁𝗿𝘆 𝗗𝗮𝘁𝗮',
        'get_num_btn': '📞 𝗚𝗲𝘁 𝗡𝘂𝗺𝗯𝗲𝗿',
        'official_channel': '📢 𝗢𝗳𝗳𝗶𝗰𝗶𝗮𝗹 𝗖𝗵𝗮𝗻𝗻𝗲𝗹',
        'info_update': "ℹ️ 𝗙𝗼𝗿 𝘂𝗽𝗱𝗮𝘁𝗲𝘀, 𝘂𝘀𝗲 𝘁𝗵𝗲 𝗯𝘂𝘁𝘁𝗼𝗻 𝗯𝗲𝗹𝗼𝘄:",
        'no_numbers': "📭 𝗡𝗼 𝗻𝘂𝗺𝗯𝗲𝗿𝘀 𝗮𝗿𝗲 𝗮𝘃𝗮𝗶𝗹𝗮𝗯𝗹𝗲 𝗿𝗶𝗴𝗵𝘁 𝗻𝗼𝘄.\n⏳ 𝗣𝗹𝗲𝗮𝘀𝗲 𝘁𝗿𝘆 𝗮𝗴𝗮𝗶𝗻 𝗹𝗮𝘁𝗲𝗿.",
        'select_country': "🌍 𝗦𝗲𝗹𝗲𝗰𝘁 𝗮 𝗰𝗼𝘂𝗻𝘁𝗿𝘆 𝘁𝗼 𝗴𝗲𝘁 𝗮 𝗻𝘂𝗺𝗯𝗲𝗿:",
        'wait_otp': "⌛ 𝗪𝗮𝗶𝘁𝗶𝗻𝗴 𝗳𝗼𝗿 𝗢𝗧𝗣... 🔐",
        'click_copy': "💡 𝗧𝗮𝗽 𝗼𝗻 𝘁𝗵𝗲 𝗻𝘂𝗺𝗯𝗲𝗿 𝘁𝗼 𝗰𝗼𝗽𝘆",
        'otp_group': "💬 OTP GROUP",
        'change_num': "🔁 Change Number",
        'change_country': "♻️ Change Country",
        'check_otp': "🔄 Check OTP (API)",
        'no_otp_yet': "❌ OTP not found yet on server. Try again in 5s.",
        'otp_found': "✅ 𝗢𝗧𝗣 𝗥𝗘𝗖𝗘𝗜𝗩𝗘𝗗!\n\n💬 Message: <b>{}</b>\n\n🔢 Code: <code>{}</code>",
        'set_lang': "🌐 Language set to English",
        'choose_lang': "🌐 Please select your language / Silakan pilih bahasa:"
    },
    'id': {
        'start': "【 𝗜𝗟𝗬 𝗢𝗧𝗣 𝗕𝗢𝗧 】\n\n→ 𝗣𝗶𝗹𝗶𝗵 𝗼𝗽𝘀𝗶 𝗱𝗮𝗿𝗶 𝗺𝗲𝗻𝘂 𝗱𝗶 𝗯𝗮𝘄𝗮𝗵 👇",
        'upload_btn': '📤 𝗨𝗽𝗹𝗼𝗮𝗱 𝗡𝗼𝗺𝗼𝗿',
        'status_btn': '📊 𝗦𝘁𝗮𝘁𝘂𝘀 𝗣𝗮𝗻𝗲𝗹',
        'reset_btn': '♻️ 𝗥𝗲𝘀𝗲𝘁 𝗦𝗲𝗺𝘂𝗮 𝗗𝗮𝘁𝗮',
        'del_country_btn': '🗑 𝗛𝗮𝗽𝘂𝘀 𝗗𝗮𝘁𝗮 𝗡𝗲𝗴𝗮𝗿𝗮',
        'get_num_btn': '📞 𝗔𝗺𝗯𝗶𝗹 𝗡𝗼𝗺𝗼𝗿',
        'official_channel': '📢 𝗖𝗵𝗮𝗻𝗻𝗲𝗹 𝗥𝗲𝘀𝗺𝗶',
        'info_update': "ℹ️ 𝗨𝗻𝘁𝘂𝗸 𝘂𝗽𝗱𝗮𝘁𝗲, 𝗴𝘂𝗻𝗮𝗸𝗮𝗻 𝘁𝗼𝗺𝗯𝗼𝗹 𝗱𝗶 𝗯𝗮𝘄𝗮𝗵:",
        'no_numbers': "📭 𝗧𝗶𝗱𝗮𝗸 𝗮𝗱𝗮 𝗻𝗼𝗺𝗼𝗿 𝘁𝗲𝗿𝘀𝗲𝗱𝗶𝗮 𝘀𝗮𝗮𝘁 𝗶𝗻𝗶.\n⏳ 𝗦𝗶𝗹𝗮𝗸𝗮𝗻 𝗰𝗼𝗯𝗮 𝗹𝗮𝗴𝗶 𝗻𝗮𝗻𝘁𝗶.",
        'select_country': "🌍 𝗣𝗶𝗹𝗶𝗵 𝗻𝗲𝗴𝗮𝗿𝗮 𝘂𝗻𝘁𝘂𝗸 𝗺𝗲𝗻𝗴𝗮𝗺𝗯𝗶𝗹 𝗻𝗼𝗺𝗼𝗿:",
        'wait_otp': "⌛ 𝗠𝗲𝗻𝘂𝗻𝗴𝗴𝘂 𝗢𝗧𝗣... 🔐",
        'click_copy': "💡 𝗧𝗲𝗸𝗮𝗻 𝗻𝗼𝗺𝗼𝗿 𝘂𝗻𝘁𝘂𝗸 𝗺𝗲𝗻𝘆𝗮𝗹𝗶𝗻",
        'otp_group': "💬 GRUP OTP",
        'change_num': "🔁 Ganti Nomor",
        'change_country': "♻️ Ganti Negara",
        'check_otp': "🔄 Cek OTP (API)",
        'no_otp_yet': "❌ OTP belum masuk di server. Coba lagi dalam 5 detik.",
        'otp_found': "✅ 𝗢𝗧𝗣 𝗗𝗜𝗧𝗘𝗥𝗜𝗠𝗔!\n\n💬 Pesan: <b>{}</b>\n\n🔢 Kode: <code>{}</code>",
        'set_lang': "🌐 Bahasa diatur ke Indonesia",
        'choose_lang': "🌐 Silakan pilih bahasa / Please select your language:"
    }
}

def get_str(user_id, key):
    lang = user_languages.get(str(user_id), 'en')
    return LANG[lang].get(key, key)

# ===== Persistence =====
def save_data():
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump({
                'country_numbers': country_numbers,
                'user_numbers': {
                    str(uid): {c: list(nums) for c, nums in cn.items()}
                    for uid, cn in user_numbers.items()
                },
                'used_numbers_global': {
                    c: list(nums) for c, nums in used_numbers_global.items()
                },
                'user_languages': user_languages
            }, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f'⚠️ Save error: {e}')

def load_data():
    global country_numbers, user_numbers, used_numbers_global, user_languages
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                country_numbers = data.get('country_numbers', {})
                used_numbers_global = {
                    c: set(nums)
                    for c, nums in data.get('used_numbers_global', {}).items()
                }
                user_numbers = {
                    int(uid): {c: set(nums) for c, nums in cn.items()}
                    for uid, cn in data.get('user_numbers', {}).items()
                }
                user_languages = data.get('user_languages', {})
        except Exception as e:
            print(f'⚠️ Corrupt data file: {e}, resetting...')
            country_numbers, user_numbers, used_numbers_global, user_languages = {}, {}, {}, {}
            save_data()

# ===== Utils =====
def is_admin(user_id):
    return user_id in ADMIN_IDS

def get_new_number(user_id, country):
    available = [
        n for n in country_numbers.get(country, [])
        if n not in used_numbers_global.get(country, set())
    ]
    if not available:
        return None
    num = available[0]
    used_numbers_global.setdefault(country, set()).add(num)
    user_numbers.setdefault(user_id, {}).setdefault(country, set()).add(num)
    country_numbers[country].remove(num)
    save_data()
    return num

def check_api_for_sms(phone_number):
    try:
        params = {
            'token': API_TOKEN,
            'records': 200
        }
        resp = requests.get(API_URL, params=params, timeout=10)
        data = resp.json()
        
        if data.get('status') == 'success':
            messages = data.get('data', [])
            clean_phone = phone_number.replace('+', '').replace(' ', '').strip()
            
            for msg in messages:
                api_num = str(msg.get('num', '')).strip()
                if api_num == clean_phone:
                    text_msg = msg.get('message', '')
                    import re
                    code_match = re.search(r'\b\d{4,8}\b', text_msg)
                    code = code_match.group(0) if code_match else "N/A"
                    return True, text_msg, code
        return False, None, None
    except Exception as e:
        print(f"API Error: {e}")
        return False, None, None

# ===== Keyboards =====
def lang_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🇺🇸 English", callback_data="set_lang|en"),
        types.InlineKeyboardButton("🇮🇩 Indonesia", callback_data="set_lang|id")
    )
    return markup

def main_keyboard(user_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    if is_admin(user_id):
        markup.add(get_str(user_id, 'upload_btn'), get_str(user_id, 'status_btn'))
        markup.add(get_str(user_id, 'reset_btn'), get_str(user_id, 'del_country_btn'))
    markup.add(get_str(user_id, 'get_num_btn'))
    return markup

def get_country_inline():
    markup = types.InlineKeyboardMarkup(row_width=2)
    for country in country_numbers.keys():
        markup.add(
            types.InlineKeyboardButton(country, callback_data=f'select_country|{country}')
        )
    return markup

def get_country_delete_inline():
    markup = types.InlineKeyboardMarkup(row_width=2)
    for country in country_numbers.keys():
        markup.add(
            types.InlineKeyboardButton(country, callback_data=f'delete_country|{country}')
        )
    return markup

# ===== Start =====
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    if str(user_id) not in user_languages:
        bot.send_message(message.chat.id, LANG['en']['choose_lang'], reply_markup=lang_keyboard())
    else:
        show_main_menu(message)

def show_main_menu(message):
    user_id = message.from_user.id
    bot.send_message(
        message.chat.id,
        get_str(user_id, 'start'),
        reply_markup=main_keyboard(user_id)
    )

    info_markup = types.InlineKeyboardMarkup()
    info_markup.add(
        types.InlineKeyboardButton(get_str(user_id, 'official_channel'), url=CHANNEL_LINK),
    )
    bot.send_message(
        message.chat.id,
        get_str(user_id, 'info_update'),
        reply_markup=info_markup
    )

# ===== Number Distribution =====
def send_number_edit(user_id, chat_id, message_id, country):
    num = get_new_number(user_id, country)
    if num is None:
        text = (
            f"❌ 𝗡𝗼 𝗺𝗼𝗿𝗲 𝗮𝘃𝗮𝗶𝗹𝗮𝗯𝗹𝗲 𝗻𝘂𝗺𝗯𝗲𝗿𝘀 𝗳𝗼𝗿 {country}.\n"
            "⏳ 𝗣𝗹𝗲𝗮𝘀𝗲 𝘄𝗮𝗶𝘁 𝗳𝗼𝗿 𝗮𝗱𝗺𝗶𝗻 𝘁𝗼 𝘂𝗽𝗹𝗼𝗮𝗱 𝗻𝗲𝘄 𝗻𝘂𝗺𝗯𝗲𝗿𝘀."
        )
        try:
            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text)
        except:
            bot.send_message(chat_id, text)
        return

    import re
    num_clean = re.sub(r'\D', '', str(num))
    num_safe = html.escape(str(num))
    
    markup = types.InlineKeyboardMarkup()
    # Gunakan num_clean agar callback_data tetap pendek (di bawah 64 byte)
    markup.row(types.InlineKeyboardButton(get_str(user_id, 'check_otp'), callback_data=f"otp|{num_clean}"))
    markup.row(types.InlineKeyboardButton(get_str(user_id, 'otp_group'), url=GROUP_LINK))
    markup.row(types.InlineKeyboardButton(get_str(user_id, 'change_num'), callback_data=f"change_num|{country}"))
    markup.row(types.InlineKeyboardButton(get_str(user_id, 'change_country'), callback_data="change_country"))

    text = (
        f"🌍 𝗖𝗼𝘂𝗻𝘁𝗿𝘆: <b>{country}</b>\n\n"
        "──────────  Number  ──────────\n"
        f"           <code>{num_safe}</code>\n"
        "──────────────────────────────\n\n"
        f"{get_str(user_id, 'wait_otp')}\n\n"
        f"{get_str(user_id, 'click_copy')}"
    )

    try:
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, parse_mode='HTML', reply_markup=markup)
    except:
        bot.send_message(chat_id, text, parse_mode='HTML', reply_markup=markup)

# ===== Button Handlers =====
@bot.message_handler(func=lambda msg: True)
def handle_buttons(message):
    user_id = message.from_user.id
    text = message.text
    
    # Admin & User buttons mapped to text
    if text == get_str(user_id, 'upload_btn') and is_admin(user_id):
        msg = bot.send_message(
            message.chat.id,
            "🌍 𝗘𝗻𝘁𝗲𝗿 𝗖𝗢𝗨𝗡𝗧𝗥𝗬 𝗡𝗔𝗠𝗘 (𝗲.𝗴. 𝗨𝗦𝗔, 𝗜𝗡𝗗𝗜𝗔, 𝗨𝗞):"
        )
        bot.register_next_step_handler(msg, ask_country_name)

    elif text == get_str(user_id, 'status_btn') and is_admin(user_id):
        total_users = len(user_numbers)
        active_countries = {
            c for c in list(country_numbers.keys()) + list(used_numbers_global.keys())
            if (c in country_numbers and country_numbers[c])
            or (c in used_numbers_global and used_numbers_global[c])
        }
        if not active_countries:
            bot.send_message(message.chat.id, "📭 𝗡𝗼 𝗰𝗼𝘂𝗻𝘁𝗿𝘆 𝗱𝗮𝘁𝗮 𝗳𝗼𝘂𝗻𝗱.")
            return

        status = (
            "📊 【 𝗜𝗟𝗬 𝗢𝗧𝗣 𝗣𝗔𝗡𝗘𝗟 𝗦𝗧𝗔𝗧𝗨𝗦 】\n\n"
            f"👤 𝗧𝗼𝘁𝗮𝗹 𝗨𝘀𝗲𝗿𝘀: {total_users}\n"
            f"🌎 𝗔𝗰𝘁𝗶𝘃𝗲 𝗖𝗼𝘂𝗻𝘁𝗿𝗶𝗲𝘀: {len(active_countries)}\n\n"
        )

        for country in active_countries:
            added = len(country_numbers.get(country, [])) + len(used_numbers_global.get(country, []))
            used = len(used_numbers_global.get(country, []))
            remaining = len(country_numbers.get(country, []))
            status += (
                f"🌍 {country}\n"
                f"📥 𝗧𝗼𝘁𝗮𝗹 𝗔𝗱𝗱𝗲𝗱: {added}\n"
                f"✅ 𝗨𝘀𝗲𝗱: {used}\n"
                f"🕓 𝗥𝗲𝗺𝗮𝗶𝗻𝗶𝗻𝗴: {remaining}\n\n"
            )
        bot.send_message(message.chat.id, status)

    elif text == get_str(user_id, 'reset_btn') and is_admin(user_id):
        country_numbers.clear()
        used_numbers_global.clear()
        user_numbers.clear()
        save_data()
        bot.send_message(message.chat.id, "♻️ 𝗔𝗹𝗹 𝗱𝗮𝘁𝗮 𝗵𝗮𝘀 𝗯𝗲𝗲𝗻 𝗰𝗹𝗲𝗮𝗿𝗲𝗱 𝘀𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆.")

    elif text == get_str(user_id, 'del_country_btn') and is_admin(user_id):
        if not country_numbers:
            bot.send_message(message.chat.id, "📭 No data.")
            return
        bot.send_message(
            message.chat.id,
            "🗑 𝗦𝗲𝗹𝗲𝗰𝘁 𝘁𝗵𝗲 𝗰𝗼𝘂𝗻𝘁𝗿𝘆 𝘁𝗼 𝗱𝗲𝗹𝗲𝘁𝗲:",
            reply_markup=get_country_delete_inline()
        )

    elif text == get_str(user_id, 'get_num_btn'):
        if not country_numbers:
            bot.send_message(message.chat.id, get_str(user_id, 'no_numbers'))
            return
        bot.send_message(
            message.chat.id,
            get_str(user_id, 'select_country'),
            reply_markup=get_country_inline()
        )

# ===== Upload Flow =====
def ask_country_name(message):
    country = message.text.strip()
    msg = bot.send_message(
        message.chat.id,
        f"✅ 𝗖𝗼𝘂𝗻𝘁𝗿𝘆 𝘀𝗲𝘁 𝘁𝗼: <b>{country}</b>\n\n"
        "📤 𝗡𝗼𝘄 𝘀𝗲𝗻𝗱 𝗻𝘂𝗺𝗯𝗲𝗿𝘀:\n"
        "• 𝗣𝗮𝘀𝘁𝗲 𝗻𝘂𝗺𝗯𝗲𝗿𝘀 𝘀𝗲𝗽𝗮𝗿𝗮𝘁𝗲𝗱 𝗯𝘆 𝗰𝗼𝗺𝗺𝗮𝘀 (,)\n"
        "• 𝗢𝗿 𝘂𝗽𝗹𝗼𝗮𝗱 𝗮 .𝘁𝘅𝘁 𝗳𝗶𝗹𝗲",
        parse_mode='HTML'
    )
    bot.register_next_step_handler(msg, lambda m: process_numbers(m, country))

def process_numbers(message, country):
    try:
        numbers = []
        if message.text:
            text_data = message.text.replace('\n', ',')
            numbers = [n.strip() for n in text_data.split(',') if n.strip()]
        elif message.document:
            file_info = bot.get_file(message.document.file_id)
            file_content = bot.download_file(file_info.file_path).decode('utf-8', errors='ignore')
            file_content = file_content.replace('\n', ',')
            numbers = [n.strip() for n in file_content.split(',') if n.strip()]

        if not numbers:
            bot.send_message(message.chat.id, "❌ Error.")
            return

        country_numbers.setdefault(country, []).extend(numbers)
        save_data()
        bot.send_message(
            message.chat.id,
            f"✅ Added <b>{len(numbers)}</b> numbers for <b>{country}</b>",
            parse_mode='HTML'
        )
    except Exception as e:
        bot.send_message(message.chat.id, f"⚠️ Error: {e}")

# ===== Inline Callbacks =====
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    user_id = call.from_user.id
    try:
        if call.data.startswith('set_lang|'):
            _, lang = call.data.split('|')
            user_languages[str(user_id)] = lang
            save_data()
            bot.delete_message(call.message.chat.id, call.message.message_id)
            bot.send_message(call.message.chat.id, get_str(user_id, 'set_lang'))
            show_main_menu(call.message)

        elif call.data.startswith('select_country|'):
            _, country = call.data.split('|', 1)
            send_number_edit(user_id, call.message.chat.id, call.message.message_id, country)

        elif call.data.startswith('change_num|'):
            _, country = call.data.split('|', 1)
            send_number_edit(user_id, call.message.chat.id, call.message.message_id, country)

        elif call.data == 'change_country':
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=get_str(user_id, 'select_country'),
                reply_markup=get_country_inline()
            )

        elif call.data.startswith('check_otp|'):
            _, number = call.data.split('|')
            bot.answer_callback_query(call.id, "🔎 Checking API...")
            found, text_msg, code = check_api_for_sms(number)
            
            if found:
                final_text = get_str(user_id, 'otp_found').format(text_msg, code)
                bot.send_message(call.message.chat.id, final_text, parse_mode='HTML')
            else:
                bot.answer_callback_query(call.id, get_str(user_id, 'no_otp_yet'), show_alert=True)

        elif call.data.startswith('delete_country|') and is_admin(user_id):
            _, country = call.data.split('|', 1)
            country_numbers.pop(country, None)
            used_numbers_global.pop(country, None)
            save_data()
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=f"🗑 Deleted {country}."
            )
    except Exception as e:
        print(f"⚠️ Callback error: {e}")

# ===== Main Loop =====
load_data()
print("🚀 Bot started")

while True:
    try:
        bot.polling(non_stop=True, interval=1, timeout=60)
    except Exception as e:
        print(f"⚠️ Bot crashed: {e}")
        time.sleep(5)
