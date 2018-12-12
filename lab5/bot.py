import requests
import config
import telebot
import datetime as dt
import calendar
from datetime import datetime
from bs4 import BeautifulSoup


bot = telebot.TeleBot(config.access_token)


def get_page(group, week=''):
    if week:
        week = str(week) + '/'
    url = '{domain}/{group}/{week}raspisanie_zanyatiy_{group}.htm'.format(
        domain=config.domain,
        week=week,
        group=group)
    response = requests.get(url)
    web_page = response.text
    return web_page


def parse_schedule(web_page, day_number):
    soup = BeautifulSoup(web_page, "html5lib")

    # Получаем таблицу с расписанием на понедельник
    schedule_table = soup.find("table", attrs={"id": "{}day".format(day_number)})

    # Время проведения занятий
    times_list = schedule_table.find_all("td", attrs={"class": "time"})
    times_list = [time.span.text for time in times_list]

    # Место проведения занятий
    locations_list = schedule_table.find_all("td", attrs={"class": "room"})
    locations_list = [room.span.text for room in locations_list]

    # Название дисциплин и имена преподавателей
    lessons_list = schedule_table.find_all("td", attrs={"class": "lesson"})
    lessons_list = [lesson.text.split('\n\n') for lesson in lessons_list]
    lessons_list = [', '.join([info for info in lesson_info if info]) for lesson_info in lessons_list]

    return times_list, locations_list, lessons_list


@bot.message_handler(commands=['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'])
def get_schedule(message):
    """ Получить расписание на указанный день """
    day, group = message.text.split()
    web_page = get_page(group)
    days = ['/monday', '/tuesday', '/wednesday', '/thursday', '/friday', '/saturday', '/sunday']
    day_number = str(int(days.index(day)) + 1)
    times_lst, locations_lst, lessons_lst = \
        parse_schedule(web_page, day_number)
    resp = ''
    for time, location, lession in zip(times_lst, locations_lst, lessons_lst):
        resp += '<b>{}</b>, {}, {}\n'.format(time, location, lession)
    bot.send_message(message.chat.id, resp, parse_mode='HTML')


@bot.message_handler(commands=['near'])
def get_near_lesson(message):
    """ Получить ближайшее занятие """
    _, group = message.text.split()
    week_number = dt.date.today().isocalendar()[1]
    week_number = str(2 - int(week_number - 1) % 2)
    present_time = dt.datetime.now().time()
    present_time = str(present_time).split(":")
    present_time = float(present_time[0] + "." + present_time[1])
    day_number = dt.datetime.isoweekday(dt.datetime.today())
    web_page = get_page(group, week_number)
    times_lst, locations_lst, lessons_lst = \
        parse_schedule(web_page, day_number)
    resp = ''
    for time, location, lession in zip(times_lst, locations_lst, lessons_lst):
        _, finish_time = str(time).split("-")
        finish_time = str(finish_time).split(":")
        finish_time = float(finish_time[0] + "." + finish_time[1])
        if present_time < finish_time:
            resp += '<b>{}</b>, {}, {}\n'.format(time, location, lession)
    if not resp:
        times_lst, locations_lst, lessons_lst = \
            parse_schedule(web_page, day_number+1)
        for time, location, lession in zip(times_lst, locations_lst, lessons_lst):
            resp += '<b>{}</b>, {}, {}\n'.format(time, location, lession)
    bot.send_message(message.chat.id, resp, parse_mode='HTML')


@bot.message_handler(commands=['tommorow'])
def get_tommorow(message):
    """ Получить расписание на следующий день """
    _, group = message.text.split()
    week_number = dt.date.today().isocalendar()[1]
    week_number = str(2 - int(week_number - 1) % 2)
    day_number = dt.datetime.isoweekday(dt.datetime.today())
    web_page = get_page(group, week_number)
    times_lst, locations_lst, lessons_lst = \
        parse_schedule(web_page, day_number+1)
    resp = ''
    for time, location, lession in zip(times_lst, locations_lst, lessons_lst):
        resp += '<b>{}</b>, {}, {}\n'.format(time, location, lession)

    bot.send_message(message.chat.id, resp, parse_mode='HTML')


@bot.message_handler(commands=['all'])
def get_all_schedule(message):
    """ Получить расписание на всю неделю для указанной группы """
    _, group = message.text.split()
    resp = ''
    days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']
    web_page = get_page(group)
    for day_number, day in enumerate(days):
        day_resp = ''
        times_lst, locations_lst, lessons_lst = \
            parse_schedule(web_page, day_number + 1)
        for time, location, lession in zip(times_lst, locations_lst, lessons_lst):
            day_resp += '<b>{}</b>, {}, {}\n'.format(time, location, lession)
        if day_resp:
            resp += '<b>{}:</b>\n\n{}'.format(day, day_resp)
    bot.send_message(message.chat.id, resp, parse_mode='HTML')


if __name__ == '__main__':
    bot.polling(none_stop=True)
