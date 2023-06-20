import telebot
from telebot import types
import openai
import time


GPT_KEY = "KEY"
TG_KEY = "KEY"

bot = telebot.TeleBot(TG_KEY)
openai.api_key = GPT_KEY

def main():
    @bot.message_handler(commands=['start'])
    def start(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Начать чат 💬")
        btn2 = types.KeyboardButton("Нарисовать картинку 🖼️")
        markup.add(btn1, btn2)
        bot.send_message(
            message.chat.id, text="Привет, я - чатбот, созданный на основе чата GPT.", reply_markup=markup)
        
        filew = open('logs.txt', 'w', encoding='utf-8')
        filew.write(
            f'{message.from_user.username} | {message.text} | {time.strftime("%Y-%m-%d %H:%M")}')
        filew.close()


    @bot.message_handler(content_types=['text'])
    def get_text_messages(message):
        if message.text == "Начать чат 💬":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Нарисовать картину 🖼️")
            back = types.KeyboardButton("Вернуться в главное меню")
            markup.add(btn1, back)

            # Json chat
            getMessage = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": message.text}
                ]
            )
            bot.send_message(message.from_user.id,
                            getMessage.choices[0].message.content)
            
            filew = open('logs.txt', 'a', encoding='utf-8')
            filew.write(
                f'{message.from_user.username} | {message.text} | {time.strftime("%Y-%m-%d %H:%M")} \n')
            filew.close()

        elif message.text == "Вернуться в главное меню":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Начать чат 💬")
            btn2 = types.KeyboardButton("Нарисовать картинку 🖼️")
            markup.add(btn1, btn2)
            bot.send_message(
                message.chat.id, text="Вы вернулись в главное меню", reply_markup=markup)
            
            filew = open('logs.txt', 'a', encoding='utf-8')
            filew.write(
                f'{message.from_user.username} | {message.text} | {time.strftime("%Y-%m-%d %H:%M")} \n')
            filew.close()

        elif message.text == "Нарисовать картинку 🖼️":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Начать чат 💬")
            btn2 = types.KeyboardButton("Нарисовать картинку 🖼️")
            markup.add(btn1, btn2)
            bot.send_message(
                message.chat.id, text="Для создания изображения необходимо написать 'img-<ваш запрос>'", reply_markup=markup)
            
            filew = open('logs.txt', 'a', encoding='utf-8')
            filew.write(
                f'{message.from_user.username} | {message.text} | {time.strftime("%Y-%m-%d %H:%M")} \n')
            filew.close()


        elif str(message.text).split('-')[0] == 'img':
            bot.send_message(message.from_user.id, "Обработка запроса..⌛️")
            getImage = openai.Image.create(
                prompt=str(message.text).split('-')[1],
                n=2,
                size="1024x1024"
            )
            bot.delete_message(message.chat.id, message.message_id + 1)
            bot.send_photo(message.from_user.id, getImage.data[0].url)

            filew = open('logs.txt', 'a', encoding='utf-8')
            filew.write(
                f'{message.from_user.username} | {message.text} | {time.strftime("%Y-%m-%d %H:%M")} \n')
            filew.close()

        else:
            bot.send_message(message.from_user.id, "Обработка запроса..⌛️")
            # Json chat
            getMessage = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": message.text}
                ]
            )
            bot.delete_message(message.chat.id, message.message_id + 1)
            bot.send_message(message.from_user.id,
                            getMessage.choices[0].message.content)
            
            filew = open('logs.txt', 'a', encoding='utf-8')
            filew.write(
                f'{message.from_user.username} | {message.text} | {time.strftime("%Y-%m-%d %H:%M")} \n')
            filew.close()


    bot.polling(none_stop=True, interval=0)


if __name__ == '__main__':
    try:
        main()
    except:
        main()
