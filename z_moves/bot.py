import datetime
from datetime import date

import telebot
import os
import re
import schedule
from time import sleep
from threading import Thread
from z_moves.buttons import *
from z_moves.scripts.schedule_parser import *

bot = telebot.TeleBot(os.environ['BOT_TOKEN'])
sch = Schedule()

'''
########################################################################################################################
                                              KEYBOARD SECTION
########################################################################################################################                               
'''

back_button_keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
back_button_keyboard.add(back_button)

role_choose_keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
role_choose_keyboard.add(student_button, teacher_button)

re_register_keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
re_register_keyboard.add(student_button, teacher_button)
re_register_keyboard.add(back_button)

settings_keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
settings_keyboard.add(links_button, hotlines_button)
settings_keyboard.add(notifications_button, change_group_button)
settings_keyboard.add(back_button)

main_menu_keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
main_menu_keyboard.add(session_button)
main_menu_keyboard.add(current_day_button, tomorrow_day_button)
main_menu_keyboard.add(schedule_button, settings_button)
main_menu_keyboard.add(info_button, help_button)


week_choose_keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
week_choose_keyboard.add(week1_button, week2_button)
week_choose_keyboard.add(back_button)

day_choose_keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
day_choose_keyboard.add(
    day_button[0],
    day_button[1],
    day_button[2],
    day_button[3],
    day_button[4],
    back_button
)

'''
########################################################################################################################
                                                BOT START
########################################################################################################################
'''
@bot.message_handler(commands=['start'])
def start_message(message):
    try:
        bot.send_message(message.chat.id, '''
О, привет! 🥴🤙
Z-Moves на связи 😎
Для начала идентифицируй себя как "студент" или "преподаватель" 🙂    
''', reply_markup=role_choose_keyboard)
        bot.register_next_step_handler(message, callback=registration)

    except AttributeError:
        bot.send_message(message.chat.id, 'i dont understand, sorry bro')
        bot.register_next_step_handler(message, callback=registration)


@bot.message_handler(content_types=['text'])
def identification(message):
    bot.send_message(message.chat.id, 'Для начала идентифицируй себя как "студент" или "преподаватель" 🙂', reply_markup=re_register_keyboard)
    bot.register_next_step_handler(message, callback=re_registration)


@bot.message_handler(content_types=['text'])
def registration(message):
    try:
        if message.text == student_button:
            bot.send_message(message.chat.id,
                             'Привет, трудяга! Чтобы показать расписание, мне нужно узнать твою группу 🙂',
                             reply_markup=re_register_keyboard)
            bot.register_next_step_handler(message, callback=student_registration)

        elif message.text == teacher_button:
            bot.send_message(message.chat.id,
                    'Добрый день! Чтобы показать Ваше расписание, мне нужно узнать Ваше полное имя, фамилию и отчество украинском 🙂',
                    reply_markup=re_register_keyboard
            )
            bot.register_next_step_handler(message, callback=teacher_registration)
        elif message.text == back_button:
            bot.send_message(message.chat.id, 'Возвращаемся назад...', reply_markup=role_choose_keyboard)
            bot.register_next_step_handler(message, callback=re_registration)
        else:
            bot.send_message(message.chat.id, 'Не могу вас идентифицировать. Попробуйте еще раз', reply_markup=role_choose_keyboard)
            bot.register_next_step_handler(message, callback=registration)
    except AttributeError:
        bot.send_message(message.chat.id, 'i dont understand, sorry bro', reply_markup=settings_keyboard)
        bot.register_next_step_handler(message, callback=settings)


@bot.message_handler(content_types=['text'])
def re_registration(message):
    try:
        if message.text == student_button:
            bot.send_message(message.chat.id, 'Введи новую группу 🙂')
            bot.register_next_step_handler(message, callback=student_registration)

        elif message.text == teacher_button:
            bot.send_message(message.chat.id,
                    'Введите Ваше полное имя, фамилию и отчество на украинском 🙂'
            )
            bot.register_next_step_handler(message, callback=teacher_registration)
        elif message.text == back_button:
            bot.send_message(message.chat.id, 'Возвращаемся назад...', reply_markup=settings_keyboard)
            bot.register_next_step_handler(message, callback=settings)
        else:
            bot.send_message(message.chat.id, 'Не могу вас идентифицировать. Попробуйте еще раз', reply_markup=role_choose_keyboard)
            bot.register_next_step_handler(message, callback=registration)
    except AttributeError:
        bot.send_message(message.chat.id, 'i dont understand, sorry bro', reply_markup=settings_keyboard)
        bot.register_next_step_handler(message, callback=settings)

'''                        
########################################################################################################################                    
                                                 MAIN MENU TREE       
########################################################################################################################                                                       
'''

@bot.message_handler(content_types=['text'])



@bot.message_handler(content_types=['text'])
def teacher_registration(message):
    try:
        if message.text == back_button:
            bot.send_message(message.chat.id, 'Возвращаемся назад...', reply_markup=role_choose_keyboard)
            bot.register_next_step_handler(message, callback=registration)
        else:
            if sch.is_teacher_exist(message.text):
                sch.identify_as('преподаватель', message.text)
                bot.send_message(message.chat.id,
                                 'Добрый день, {0}!'.format(sch.get_teacher_name(message.text)),
                                 reply_markup=main_menu_keyboard)
                bot.register_next_step_handler(message, callback=main_menu)
            else:
                bot.send_message(message.chat.id, '''Мне не удаётся Вас распознать 🤥\nПоробуйте ещё''')
                bot.register_next_step_handler(message, callback=teacher_registration)

    except AttributeError:
        bot.send_message(message.chat.id, 'Такие данные мне подходят 🙂')
        bot.register_next_step_handler(message, callback=teacher_registration)

@bot.message_handler(content_types=['text'])
def student_registration(message):
    try:
        if message.text == back_button:
            bot.send_message(message.chat.id, 'Возвращаемся назад...', reply_markup=role_choose_keyboard)
            bot.register_next_step_handler(message, callback=registration)
        else:
            if sch.is_group_exist(message.text):
                sch.identify_as('студент', message.text)
                bot.send_message(message.chat.id, 'Есть такая! Ну а теперь приступим 🙂', reply_markup=main_menu_keyboard)
                bot.register_next_step_handler(message, callback=main_menu)
            else:
                bot.send_message(message.chat.id, '''Ой, что-то я о такой группе не слышал 🤥\nПоробуй ещё''')
                bot.register_next_step_handler(message, callback=student_registration)

    except AttributeError:
        bot.send_message(message.chat.id, 'Такие данные мне подходят 🙂')
        bot.register_next_step_handler(message, callback=student_registration)


@bot.message_handler(content_types=['text'])
def main_menu(message):

    info_message = "Имя бота: Z-Moves Bot\n\n" + \
                   "Кто авторизован: " + sch.role + "\n\n" + \
                   "Авторы:\nDanon(@danilos0)\nДимасик(@KickYourSelff)\nРостянский(@leap_sunrise)"

    try:
        if message.text == session_button:
            bot.send_message(message.chat.id, sch.get_session_for_schedule(), parse_mode='HTML', reply_markup=main_menu_keyboard)
            bot.register_next_step_handler(message, callback=main_menu)

        elif message.text == schedule_button:
            bot.send_message(message.chat.id, 'Выбери неделю', reply_markup=week_choose_keyboard)
            bot.register_next_step_handler(message, callback=week_choose)

        elif message.text == settings_button:
            bot.send_message(message.chat.id, 'Что ты желаешь настроить?', reply_markup=settings_keyboard)
            bot.register_next_step_handler(message, callback=settings)

        elif message.text == info_button:
            bot.send_message(message.chat.id, info_message, reply_markup=main_menu_keyboard)
            bot.register_next_step_handler(message, callback=main_menu)

        elif message.text == help_button:
            bot.send_message(message.chat.id, develop_button, reply_markup=main_menu_keyboard)
            bot.register_next_step_handler(message, callback=main_menu)

        elif message.text == current_day_button:
            s = show_day("Сегодня", date.today().weekday() + 1)
            bot.send_message(message.chat.id, s, parse_mode="HTML", reply_markup=main_menu_keyboard)
            bot.register_next_step_handler(message, callback=main_menu)

        elif message.text == tomorrow_day_button:
            tomorrow = (date.today() + datetime.timedelta(days=1)).weekday() + 1
            s = show_day("Завтра", tomorrow)
            bot.send_message(message.chat.id, s, parse_mode="HTML", reply_markup=main_menu_keyboard)
            bot.register_next_step_handler(message, callback=main_menu)
        else:
            bot.send_message(message.chat.id, 'i dont understand, sorry bro', reply_markup=main_menu_keyboard)
            bot.register_next_step_handler(message, callback=main_menu)
    except AttributeError:
        bot.send_message(message.chat.id, 'i dont understand, sorry bro', reply_markup=settings_keyboard)
        bot.register_next_step_handler(message, callback=settings)


'''
########################################################################################################################                                            
                                                  SCHEDULE BRANCH                   
########################################################################################################################                                                  
'''


def show_day(wd: str, day: int):
    if day > 4:
        s = wd + ' пар нету. Отдыхаем'
    else:
        weekday = week_days[day]
        cur_week = get_current_week()
        s = show_schedule(weekday, sch.get_schedule(cur_week, day), '', '', '')
    return s


@bot.message_handler(content_types=['text'])
def week_choose(message):
    try:
        if message.text == week1_button:
            bot.send_message(message.chat.id, 'А теперь день', reply_markup=day_choose_keyboard)
            bot.register_next_step_handler(message, callback=week_1)
        elif message.text == week2_button:
            bot.send_message(message.chat.id, 'А теперь день', reply_markup=day_choose_keyboard)
            bot.register_next_step_handler(message, callback=week_2)
        elif message.text == back_button:
            bot.send_message(message.chat.id, 'Возвращаемся...', reply_markup=main_menu_keyboard)
            bot.register_next_step_handler(message, callback=main_menu)
        else:
            bot.send_message(message.chat.id, 'i dont understand, sorry bro', reply_markup=week_choose_keyboard)
            bot.register_next_step_handler(message, callback=week_choose)

    except AttributeError:
        bot.send_message(message.chat.id, 'i dont understand, sorry bro', reply_markup=settings_keyboard)
        bot.register_next_step_handler(message, callback=settings)


@bot.message_handler(content_types=['text'])
def week_1(message):
    try:
        if message.text == day_button[0]:
            bot.send_message(message.chat.id, show_schedule("понедельник", sch.get_schedule(1, 1), '', '', ''),
                             parse_mode="HTML",
                             reply_markup=day_choose_keyboard)
            bot.register_next_step_handler(message, callback=week_1)
        elif message.text == day_button[1]:
            bot.send_message(message.chat.id, show_schedule("вторник", sch.get_schedule(1, 2), '', '', ''),
                             parse_mode="HTML", reply_markup=day_choose_keyboard)
            bot.register_next_step_handler(message, callback=week_1)
        elif message.text == day_button[2]:
            bot.send_message(message.chat.id, show_schedule("среду", sch.get_schedule(1, 3), '', '', ''),
                             parse_mode="HTML", reply_markup=day_choose_keyboard)
            bot.register_next_step_handler(message, callback=week_1)
        elif message.text == day_button[3]:
            bot.send_message(message.chat.id, show_schedule("четверг", sch.get_schedule(1, 4), '', '', ''),
                             parse_mode="HTML",
                             reply_markup=day_choose_keyboard)
            bot.register_next_step_handler(message, callback=week_1)
        elif message.text == day_button[4]:
            bot.send_message(
                message.chat.id, show_schedule("пятницу", sch.get_schedule(1, 5), '', '', ''),
                parse_mode="HTML",
                reply_markup=day_choose_keyboard
            )
            bot.register_next_step_handler(message, callback=week_1)
        elif message.text == back_button:
            bot.send_message(message.chat.id, text='Возвращаемся назад...', reply_markup=week_choose_keyboard)
            bot.register_next_step_handler(message, callback=week_choose)
        else:
            bot.send_message(message.chat.id, 'i dont understand, sorry bro', reply_markup=day_choose_keyboard)
            bot.register_next_step_handler(message, callback=week_1)

    except AttributeError:
        bot.send_message(message.chat.id, 'i dont understand, sorry bro', reply_markup=settings_keyboard)
        bot.register_next_step_handler(message, callback=settings)


@bot.message_handler(content_types=['text'])
def week_2(message):
    try:
        if message.text == day_button[0]:
            bot.send_message(message.chat.id, show_schedule("понедельник", sch.get_schedule(2, 1), '', '', ''),
                             parse_mode="HTML", reply_markup=day_choose_keyboard)
            bot.register_next_step_handler(message, callback=week_2)
        elif message.text == day_button[1]:
            bot.send_message(message.chat.id, show_schedule("вторник", sch.get_schedule(2, 2), '', '', ''),
                             parse_mode="HTML", reply_markup=day_choose_keyboard)
            bot.register_next_step_handler(message, callback=week_2)
        elif message.text == day_button[2]:
            bot.send_message(message.chat.id, show_schedule("среду", sch.get_schedule(2, 3), '', '', ''),
                             parse_mode="HTML", reply_markup=day_choose_keyboard)
            bot.register_next_step_handler(message, callback=week_2)
        elif message.text == day_button[3]:
            bot.send_message(message.chat.id, show_schedule("четверг", sch.get_schedule(2, 4), '', '', ''),
                             parse_mode="HTML", reply_markup=day_choose_keyboard)
            bot.register_next_step_handler(message, callback=week_2)
        elif message.text == day_button[4]:
            bot.send_message(message.chat.id, show_schedule("пятницу", sch.get_schedule(2, 5), '', '', ''),
                             parse_mode="HTML", reply_markup=day_choose_keyboard)
            bot.register_next_step_handler(message, callback=week_2)
        elif message.text == back_button:
            bot.send_message(message.chat.id, text='Возвращаемся назад...', reply_markup=week_choose_keyboard)
            bot.register_next_step_handler(message, callback=week_choose)
        else:
            bot.send_message(message.chat.id, 'i dont understand, sorry bro', reply_markup=day_choose_keyboard)
            bot.register_next_step_handler(message, callback=week_2)

    except AttributeError:
        bot.send_message(message.chat.id, 'i dont understand, sorry bro', reply_markup=settings_keyboard)
        bot.register_next_step_handler(message, callback=settings)


'''
########################################################################################################################
                                             SCHEDULE BRANCH HAVE ENDED                
########################################################################################################################
'''

'''                                            
########################################################################################################################
                                                  SETTINGS BRANCH   
########################################################################################################################                                                                 
'''


@bot.message_handler(content_types=['text'])
def settings(message):
    try:
        if message.text == links_button:
            bot.send_message(message.chat.id, develop_button, reply_markup=settings_keyboard)
            bot.register_next_step_handler(message, settings)
        elif message.text == hotlines_button:
            bot.send_message(message.chat.id, develop_button, reply_markup=settings_keyboard)
            bot.register_next_step_handler(message, settings)
        elif message.text == notifications_button.lower():
            bot.send_message(message.chat.id, 'Введите время (в формате HH:MM), в которое я пришлю уведомление',
                             reply_markup=back_button_keyboard)
            bot.register_next_step_handler(message, callback=set_notification)
        elif message.text == change_group_button:
            bot.send_message(message.chat.id, 'Для начала идентифицируй себя как "студент" или "преподаватель" 🙂',
                             reply_markup=re_register_keyboard)
            bot.register_next_step_handler(message, callback=re_registration)
        elif message.text == back_button:
            bot.send_message(message.chat.id, 'Возвращаемся...', reply_markup=main_menu_keyboard)
            bot.register_next_step_handler(message, callback=main_menu)
        else:
            bot.send_message(message.chat.id, 'i dont understand, sorry bro', reply_markup=settings_keyboard)
            bot.register_next_step_handler(message, callback=settings)

    except AttributeError:
        bot.send_message(message.chat.id, 'i dont understand, sorry bro', reply_markup=settings_keyboard)
        bot.register_next_step_handler(message, callback=settings)


is_notification_on = False


@bot.message_handler(content_types=['text'])
def set_notification(message):
    global is_notification_on
    try:
        if re.match("^(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$", message.text):
            if not is_notification_on:
                is_notification_on = True
                schedule.every().day.at(message.text).do(lambda: send_notification(message))
                bot.send_message(message.chat.id, 'Время установлено', reply_markup=settings_keyboard)
                bot.register_next_step_handler(message, callback=settings)
            else:
                bot.send_message(message.chat.id, 'Время уже установлено', reply_markup=settings_keyboard)
                bot.register_next_step_handler(message, callback=settings)

        elif message.text == back_button:
            bot.send_message(message.chat.id, 'Возвращаемся...', reply_markup=settings_keyboard)
            bot.register_next_step_handler(message, callback=settings)
        else:
            bot.send_message(message.chat.id, 'Немножечко не по формату :(', reply_markup=back_button_keyboard)
            bot.register_next_step_handler(message, callback=set_notification)

    except AttributeError:
        bot.send_message(message.chat.id, 'i dont understand, sorry bro', reply_markup=settings_keyboard)
        bot.register_next_step_handler(message, callback=settings)


def schedule_checker():
    while True:
        schedule.run_pending()
        sleep(1)


def send_notification(message):
    bot.send_message(message.chat.id, show_day("Завтра", date.today().weekday() + 1), parse_mode="HTML")
    global is_notification_on
    is_notification_on = False


notification_thread = Thread(target=schedule_checker)
notification_thread.start()

if __name__ == '__main__':
    bot.polling()
