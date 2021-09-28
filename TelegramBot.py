import telebot
import time
import Config
import sqlite3


bot = telebot.TeleBot(Config.TOKEN, parse_mode=None)

@bot.message_handler(commands=['start'])
def RegisterUser(message):
    print(message.from_user)
    chat_id = str(message.chat.id)
    dbCon = sqlite3.connect("telegramUsers.db")
    db = dbCon.cursor()
    db.execute(f"SELECT * FROM Users WHERE chat_id={chat_id}")
    if db.fetchone() is None:
        db.execute(f"INSERT INTO Users VALUES ({chat_id})")
        dbCon.commit()
        bot.send_message(chat_id, "Вы успешно подписались на рассылку!")
    else:
        bot.send_message(chat_id, "Вы уже подписаны на рассылку!")

@bot.message_handler(commands=['active'])
def isBotActive(message):
    print(message.from_user)
    chat_id = str(message.chat.id)
    bot.send_message(chat_id, "Все в порядке!")


def BotStarted():
    dbCon = sqlite3.connect("telegramUsers.db")
    db = dbCon.cursor()
    
    #Build Message
    message = "Шпион активен"

    #Send messages to all subscribers
    for chat in db.execute("SELECT chat_id FROM Users"):
        bot.send_message(chat[0], message)


message_count = 0
def SendCar(Link: str):
    global message_count
    message_count += 1
    if message_count >= 50:
        print("Bot overloaded, sleeping 15s!")
        time.sleep(15)
        message_count = 0
    dbCon = sqlite3.connect("telegramUsers.db")
    db = dbCon.cursor()
    
    #Build Message
    message = Link

    #Send messages to all subscribers
    for chat in db.execute("SELECT chat_id FROM Users"):
        bot.send_message(chat[0], message)
    

def __init__():
    dbCon = sqlite3.connect("telegramUsers.db")
    db = dbCon.cursor()
    db.execute("""
        CREATE TABLE IF NOT EXISTS Users(
            chat_id INTEGER
        )
    """)
    dbCon.commit()
    dbCon.close()

def main():
    __init__()
    BotStarted()
    bot.polling(none_stop=True)