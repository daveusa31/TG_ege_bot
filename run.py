import time
import config
import telebot
import datetime
import subprocess


bot = telebot.TeleBot(config.TOKEN)


def logger(text):
    curr_time = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    print('{} | {}\n'.format(text, curr_time))





def run_bot_loop():
    command = ["python", "main.py"]
    resp = subprocess.Popen(command, stdout=subprocess.PIPE, 
                                                    stderr=subprocess.STDOUT)
            
    resp = resp.stdout.read().decode("cp866")
    return resp





if __name__ == "__main__":
    logger("Start ege bot")
    while True:
        error = run_bot_loop()
        logger("Restart") 

       
        with open("error.txt", "w", encoding="utf-8") as f: f.write(error)
        doc = open("error.txt", "rb")
        bot.send_document(config.ADMIN_ID, doc)
        doc.close()


        time.sleep(10)



