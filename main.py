#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import config
import telebot
import requests
import functions
from telebot import types



bot = telebot.TeleBot(config.TOKEN) #В модуле config.py заполняем переменную TOKEN, токеном от тг бота
print("Bot is started.")


@bot.message_handler(commands=["start"])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(True, False)
    markup.row("📄Ответы", "🔍F.A.Q")
    markup.row("🔑Тестовая оплата", "📊Статистика")

    all_users = functions.get_all_users()
    # Проверка на наличие айди в базе
    if str(message.chat.id) not in all_users:
        with open("base.txt", "a", encoding="utf-8") as f:
            f.write("{}\n".format(message.chat.id))
    else:
        bot.send_message(message.chat.id, "Мы с вами уже знакомы!")

    bot.send_message(message.chat.id, config.start_message, reply_markup=markup, parse_mode="markdown")

    functions.message_logger(message.text, message.from_user.username)


@bot.message_handler(commands=["rasl"])
def sending_message(message):
    if message.chat.id == config.ADMIN_ID:
        text = message.text[6:]

        good = 0
        luse = 0

        for chat_id in functions.get_all_users():
            try:
                bot.send_message(chat_id, text, parse_mode="HTML")
                good += 1

            except:
                luse += 1

        bot.send_message(message.chat.id, "{} юзеров забанили бота\n{} не забанило".format(luse, good))


@bot.message_handler(commands=["raslb"])
def sending_buyer_message(message):
    if message.chat.id == config.ADMIN_ID:
        text = message.text[6:]
        
        good = 0
        luse = 0

        for chat_id in functions.get_buyers():
            try:
                bot.send_message(chat_id, text, parse_mode="HTML")
                good += 1

            except:
                luse += 1

        bot.send_message(message.chat.id, "{} юзеров забанили бота\n{} не забанило".format(luse, good))







@bot.message_handler(content_types=['text'])
def messages(message):
    chat_id = message.from_user.id
    

    if message.text == "📊Статистика":
        with open("pays_base.txt","r", encoding="utf-8") as f:
            base = f.read().split("\n")
    
        bot.send_message(chat_id,"*В этом году, успешно сдадут экзамены*: {} человек".format(len(base)),parse_mode="markdown")

    elif message.text == "🔍F.A.Q":
        bot.send_message(chat_id,"*Преимущества работы с нами:*\n\n|_Работаем около 2 лет_\n|_300+ отзывов_\n|_Постоянная поддержка в канале_\n|_Ответы на все регионы_\n\n*Ответы на частые вопросы*\n\n-Будет ли возврат средств при неверности ответов?\n-_Да, будет, но при указании вашего региона при общении со службой поддержки_\n-За какое время до ЕГЭ, выкладываются ответы?\n-_Ответы выкладываются, от 11 до 24 часов, перед экзаменом._\n-Если ответов так и не оказалось, что мне делать?\n-_Во первых, без паники, возможно ваши ответы просто не выложили, если осталось менее 7 часов, свяжитесь со службой поддержки через группу, в случае отсутствия ваших ответов, будет возврат средств._",parse_mode="markdown")

    elif message.text == "📄Ответы":
        link = functions.get_payment_link(config.price, config.qiwi_number, message.chat.id)

        markup = types.InlineKeyboardMarkup()
        button_buy = types.InlineKeyboardButton(text="Купить ответы", url=link)
        buy_check = types.InlineKeyboardButton(text="Проверить оплату", callback_data="payment_check")
        markup.row(button_buy,buy_check)
        bot.send_message(chat_id, "*После покупки*, вы будете добавлены в специальный канал и чат, где будут обсуждаться и выкладываться ответы.\n\nОтветы выкладываются за день/за максимум 11 часов до экзамены\n\n*|Цена = {}р*\nДля оплаты нажмите на кнопку 'Купить ответы', после оплаты - нажмите 'Проверить оплату'".format(config.price),reply_markup=markup,parse_mode="markdown")


    elif message.text == "🔑Тестовая оплата":
        link = functions.get_payment_link(config.test_price, config.qiwi_number, message.chat.id)

        markup = types.InlineKeyboardMarkup()
        button_buy = types.InlineKeyboardButton(text="Купить ответы", callback_data="payment", url=link)
        buy_check = types.InlineKeyboardButton(text="Проверить оплату", callback_data="payment_check_test")
        markup.row(button_buy,buy_check)
        bot.send_message(chat_id,"*Тестовая оплата, предназначена для того, чтобы не было каких-либо инцидентов во время оплаты, здесь, вы можете попробовать совершить оплату, и проверить ее наличие в боте.*\n\n _Стоимость тестовой оплаты - 1руб_ \n\n_После оплаты - нажмите 'Проверить оплату'_",reply_markup=markup,parse_mode="markdown")

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    chat_id = call.from_user.id
    
    if call.data == "payment_check":
        url = "https://edge.qiwi.com/payment-history/v2/persons/{0}/payments".format(str(config.qiwi_number))
        headers = {"Accept": "application/json", "Content-Type": "application/json", "Authorization": "Bearer " + config.qiwi_token}
        req = requests.get(url, params={"rows": 1, "operation": "IN"}, headers=headers)

        js = json.dumps(req)
        js = json.loads(js)
        description = js["data"][0]["comment"]
        payment_last = js["data"][0]["sum"]["amount"]

        if str(description) == str(chat_id) and payment_last == config.price:
            bot.send_message(chat_id, "*Оплата получена!*\n\n_За две недели до экзаменов вы будете добавлены в чат, и приглашены в группу с ответами. Спасибо за покупку!_\n\nДоступ к группе и чату выдается пожизненно, конечно же, при соблюдении правил чата.",parse_mode="markdown")
            
            with open("pays_base.txt", "a", encoding="utf-8") as f:
                f.write("{}\n".format(chat_id))

        else:
            bot.send_message(chat_id, "*К сожалению*, оплата не получена. _Попробуйте через пару секунд._", parse_mode="markdown")


    if call.data == "payment_check_test":
        url = "https://edge.qiwi.com/payment-history/v2/persons/{0}/payments".format(str(config.qiwi_number))
        headers = {"Accept": "application/json", "Content-Type": "application/json", "Authorization": "Bearer " + config.qiwi_token}
        req = requests.get(url, params={"rows": 1, "operation": "IN"}, headers=headers)

        js = json.dumps(req)
        js = json.loads(js)
        description = js["data"][0]["comment"]

        if str(description) == str(chat_id):
            bot.send_message(chat_id, "*Оплата получена!*", parse_mode="markdown")
        elif str(description) != str(chat_id):
            bot.send_message(chat_id, "*К сожалению*, оплата не получена. _Попробуйте через пару секунд._", parse_mode="markdown")
    


bot.polling()
