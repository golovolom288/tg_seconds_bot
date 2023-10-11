import ptbot
import os

from dotenv import load_dotenv
from pytimeparse import parse


def render_progressbar(total, iteration, prefix='', suffix='', length=30, fill='█', zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)


def notify_progress(time_left, chat_id, id, time):
    bot.update_message(chat_id, id, "Осталось {0} секунд\n{1}".format(time_left, render_progressbar(time, time-time_left)))


def start_countdown(chat_id,question):
    time = parse(question)
    id_message = bot.send_message(chat_id, f"Осталось {time} секунд\n{render_progressbar(time,0)}")
    bot.create_countdown(time, notify_progress, chat_id=chat_id, id=id_message, time=time)
    bot.create_timer(time, choose, chat_id=chat_id)


def choose(chat_id):
    bot.send_message(chat_id, "Время вышло!")


if __name__ == "__main__":
    load_dotenv()
    tg_token = os.getenv("TG_TOKEN")
    tg_chat_id = os.getenv("TG_CHAT_ID")
    bot = ptbot.Bot(tg_token)
    bot.send_message(tg_chat_id, "Бот запущен")
    bot.reply_on_message(start_countdown)
    bot.run_bot()

