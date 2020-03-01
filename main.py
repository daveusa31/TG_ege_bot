#!/usr/bin/python
# -*- coding: utf-8 -*-
import telebot
from telebot import types
import const
import requests
import json

r_k = True
bot = telebot.TeleBot(const.TOKEN) #в модуле const.py заполняем переменную TOKEN, токеном от тг бота
print("| Бот инициализирован.")

markdown = const.MARKDOWN



@bot.message_handler(content_types=['text'])
def messages(message):
	userid = str(message.from_user.id)
	username = message.from_user.username
	print(message.text + " | @" + username)
	def get_payment_link(pay,number=const.NUMBER):
		payment = "https://qiwi.com/payment/form/99?extra%5B%27account%27%5D="+number+"&amountInteger=" + pay + "&amountFraction=0&extra%5B%27comment%27%5D="+userid+"&currency=643&blocked[0]=sum&blocked[1]=comment&blocked[2]=account"
		return payment


	if "/start" == message.text:
		markup = types.ReplyKeyboardMarkup(r_k)
		markup.row("📄Ответы","🔍F.A.Q")
		markup.row("🔑Тестовая оплата","📊Статистика")

		base_check = open("base.txt","r").read()
		#проверка на наличие айди в базе
		if userid not in base_check:
			#запись нового айди в базу
			base = open("base.txt","a")
			base.write("\n"+userid)
		if userid in base_check:
			bot.send_message(userid,"Мы с вами уже знакомы!")

		bot.send_message(userid,"Текст",reply_markup=markup,parse_mode="markdown")

	if "отослать" in message.text:
		if const.ADMIN != userid:
			bot.send_message("Неизвестная команда!")
		if const.ADMIN == userid:
			try:
				base = open("base.txt","r").read()
				splitter = message.text.split("/")
				splitter_of_base = base.split("\n")
				text = splitter[1]
				user_str = 0
				print(splitter_of_base)
				for user in splitter_of_base:
					bot.send_message(user,text)
			except Exception as E:
				bot.send_message(userid,"Произошла ошибка!")
				print(E)


	if message.text == "📊Статистика":
		base = open("pays_base.txt","r").read().split("\n")
		print(len(base))
		bot.send_message(userid,"*В этом году, успешно сдадут экзамены*: "+str(len(base)-1) + " человек",parse_mode="markdown")

	if message.text == "🔍F.A.Q":
		bot.send_message(userid,"*Преимущества работы с нами:*\n\n|_Работаем около 2 лет_\n|_300+ отзывов_\n|_Постоянная поддержка в канале_\n|_Ответы на все регионы_\n\n*Ответы на частые вопросы*\n\n-Будет ли возврат средств при неверности ответов?\n-_Да, будет, но при указании вашего региона при общении со службой поддержки_\n-За какое время до ЕГЭ, выкладываются ответы?\n-_Ответы выкладываются, от 11 до 24 часов, перед экзаменом._\n-Если ответов так и не оказалось, что мне делать?\n-_Во первых, без паники, возможно ваши ответы просто не выложили, если осталось менее 7 часов, свяжитесь со службой поддержки через группу, в случае отсутствия ваших ответов, будет возврат средств._",parse_mode="markdown")

	if message.text == "📄Ответы":
		markup = types.InlineKeyboardMarkup(row_width=1)
		link = get_payment_link("300",const.NUMBER)
		button_buy = types.InlineKeyboardButton(text="Купить ответы",callback_data="payment",url=link)
		buy_check = types.InlineKeyboardButton(text="Проверить оплату",callback_data="payment_check")
		markup.row(button_buy,buy_check)
		bot.send_message(userid,"*После покупки*, вы будете добавлены в специальный канал и чат, где будут обсуждаться и выкладываться ответы.\n\nОтветы выкладываются за день/за максимум 11 часов до экзамены\n\n*|Цена = 300р*\nДля оплаты нажмите на кнопку 'Купить ответы', после оплаты - нажмите 'Проверить оплату'",reply_markup=markup,parse_mode="markdown")


	if message.text == "🔑Тестовая оплата":
		markup = types.InlineKeyboardMarkup(row_width=1)
		link = get_payment_link("1",const.NUMBER)
		button_buy = types.InlineKeyboardButton(text="Купить ответы",callback_data="payment",url=link)
		buy_check = types.InlineKeyboardButton(text="Проверить оплату",callback_data="payment_check_test")
		markup.row(button_buy,buy_check)
		bot.send_message(userid,"*Тестовая оплата, предназначена для того, чтобы не было каких-либо инцидентов во время оплаты, здесь, вы можете попробовать совершить оплату, и проверить ее наличие в боте.*\n\n _Стоимость тестовой оплаты - 1руб_ \n\n_После оплаты - нажмите 'Проверить оплату'_",reply_markup=markup,parse_mode="markdown")

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
	userid = call.from_user.id
	
	if call.data == "payment_check":
		url = "https://edge.qiwi.com/payment-history/v2/persons/{0}/payments".format(str(const.NUMBER))
		headers = {"Accept": "application/json", "Content-Type": "application/json", "Authorization": "Bearer " + const.QIWI_T}
		req = requests.get(url, params={"rows": 1, "operation": "IN"}, headers = headers)
		if req.status_code == 200:
			req = req.json()

		js = json.dumps(req)
		js = json.loads(js)
		description = js["data"][0]["comment"]
		payment_last = js["data"][0]["sum"]["amount"]
		if str(description) == str(userid) and payment_last==300:
			bot.send_message(userid,"*Оплата получена!*\n\n_За две недели до экзаменов вы будете добавлены в чат, и приглашены в группу с ответами. Спасибо за покупку!_\n\nДоступ к группе и чату выдается пожизненно, конечно же, при соблюдении правил чата.",parse_mode="markdown")
			base = open("pays_base.txt","a")
			base.write("\n"+str(userid))
		if str(description) != str(userid):
			bot.send_message(userid,"*К сожалению*, оплата не получена. _Попробуйте через пару секунд._",parse_mode="markdown")


	if call.data == "payment_check_test":
		url = "https://edge.qiwi.com/payment-history/v2/persons/{0}/payments".format(str(const.NUMBER))
		headers = {"Accept": "application/json", "Content-Type": "application/json", "Authorization": "Bearer " + const.QIWI_T}
		req = requests.get(url, params={"rows": 1, "operation": "IN"}, headers = headers)
		if req.status_code == 200:
			req = req.json()

		js = json.dumps(req)
		js = json.loads(js)
		description = js["data"][0]["comment"]

		if str(description) == str(userid):
			bot.send_message(userid,"*Оплата получена!*",parse_mode="markdown")
		if str(description) != str(userid):
			bot.send_message(userid,"*К сожалению*, оплата не получена. _Попробуйте через пару секунд._",parse_mode="markdown")
	


bot.polling(none_stop=True,interval=0)
