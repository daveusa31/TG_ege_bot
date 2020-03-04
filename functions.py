def get_payment_link(sum,  number, comment):
	link = "https://qiwi.com/payment/form/99?extra%5B%27account%27%5D={}&amountInteger={}&amountFraction=0&extra%5B%27comment%27%5D={}&currency=643&blocked[0]=sum&blocked[1]=comment&blocked[2]=account"
	link = link.format(number, sum, comment)
	return link

def message_logger(text, username):
	# Файл уже создан
	try:
		with open("log.txt", "a", encoding="utf-8") as f:
			f.write("{} | @{}\n".format(text, username))

	# Создаём файл
	except:
		with open("log.txt", "w", encoding="utf-8") as f:
			f.write("{} | @{}\n".format(text, username))


def get_all_users(file="base.txt"):
	with open(file, "r", encoding="utf-8") as f:
		users = f.read()

	users = users.split("\n")

	return users[:-1]


def get_buyers(file="pays_base.txt"):
	with open(file, "r", encoding="utf-8") as f:
		users = f.read()

	users = users.split("\n")

	return users[:-1]

	