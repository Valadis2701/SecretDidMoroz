import json
import random
import telebot
import os
from typing import List



# Отримання значень токена бота та ID адміністратора з змінних середовища
BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = ADMIN_ID = os.getenv('ADMIN_ID')



bot = telebot.TeleBot(BOT_TOKEN)
json_file_path = "user_profiles.json"

@bot.message_handler(commands=['start'])
def start(message):
    telegram_id = message.from_user.id

    user_profiles = load_user_profiles()

    if str(telegram_id) in user_profiles:
        bot.send_message(telegram_id, "Ваша анкета вже зареєстрована! Щоб видалити її, використайте команду /delete_profile")
    else:
        user_profiles[str(telegram_id)] = {"name": "", "profile": ""}
        save_user_profiles(user_profiles)

        bot.send_message(telegram_id, "Привіт! Як тебе звати?")
        bot.register_next_step_handler(message, process_name)

def process_name(message):
    telegram_id = message.from_user.id
    user_profiles = load_user_profiles()

    if str(telegram_id) in user_profiles:
        user_profiles[str(telegram_id)]["name"] = message.text
        save_user_profiles(user_profiles)

        bot.send_message(telegram_id, "Чудово! Тепер опиши себе короткою анкетою. Твої хобі, інтереси або побажання. Це допоможе підібрати для тебе найкращий подарунок!")
        bot.register_next_step_handler(message, process_profile)
    else:
        bot.send_message(telegram_id, "Упс! Сталася помилка!")

def process_profile(message):
    telegram_id = message.from_user.id
    user_profiles = load_user_profiles()

    if str(telegram_id) in user_profiles:
        user_profiles[str(telegram_id)]["profile"] = message.text
        save_user_profiles(user_profiles)

        bot.send_message(telegram_id, "Дякую за реєстрацію! Скоро вам прийде повідомлення з іменем та анкетою випадкової людини")
    else:
        bot.send_message(telegram_id, "Упс! Сталася помилка!")

def load_user_profiles():
    try:
        with open(json_file_path, 'r') as file:
            user_profiles = json.load(file)
    except FileNotFoundError:
        user_profiles = {}
    return user_profiles

def save_user_profiles(user_profiles):
    with open(json_file_path, 'w') as file:
        json.dump(user_profiles, file, indent=2)

@bot.message_handler(commands=['delete_profile'])
def delete_profile(message):
    telegram_id = message.from_user.id
    user_profiles = load_user_profiles()

    if str(telegram_id) in user_profiles:
        del user_profiles[str(telegram_id)]
        save_user_profiles(user_profiles)

        bot.send_message(telegram_id, "Вашу анкету видалено. Для створення нової використовуйте команду /start")
    else:
        bot.send_message(telegram_id, "Вашу анкету не знайдено. Для створення нової використовуйте команду /start")

@bot.message_handler(commands=['begin'])
def start_santa(message):
    telegram_id = message.from_user.id

    if int(telegram_id) != int(ADMIN_ID):
        bot.send_message(telegram_id, "Ноу ноу ноу, містер Фіш...")
        return

    user_profiles = load_user_profiles()

    if len(user_profiles) < 2:
        bot.send_message(telegram_id, "Недостатньо зареєстрованих користувачів.")
    else:
        bot.send_message(telegram_id, "Запускаємо процес вибору подарунків...")

        user_ids = list(user_profiles.keys())
        random.shuffle(user_ids)
        send_gifts(user_ids, user_profiles)

def send_gifts(user_ids: List[str], user_profiles: dict):
    n = len(user_ids)
    for i in range(n):
        sender_id = user_ids[i]
        receiver_id = user_ids[(i + 1) % n]  # Визначаємо отримувача

        sender_name = user_profiles[sender_id]["name"]
        receiver_name = user_profiles[receiver_id]["name"]

        bot.send_message(sender_id, f"Ви таємний Дід Мороз для: {receiver_name}\nАнкета: {user_profiles[receiver_id]['profile']}")

bot.polling(none_stop=True)
