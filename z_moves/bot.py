import datetime
from datetime import date

import telebot
import os
import re
import schedule
from z_moves.scripts.session_db import *
from time import sleep
from threading import Thread
from z_moves.buttons import *
from z_moves.scripts.schedule_parser import *

bot = telebot.TeleBot(os.environ['BOT_TOKEN'])
sch = Schedule()
db.init_db()

'''
########################################################################################################################
                                              KEYBOARD SECTION BEGINNING
########################################################################################################################                               
'''

back_button_keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
back_button_keyboard.add(back_button)

role_choose_keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
role_choose_keyboard.add(student_button, teacher_button)

change_group_role_keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
change_group_role_keyboard.add(change_only_group_button, change_only_role_button)
change_group_role_keyboard.add(back_button)

role_change_keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
role_change_keyboard.add(student_button, teacher_button)
role_change_keyboard.add(back_button)

group_change_keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
group_change_keyboard.add(back_button)

student_change_group_role_keyboard = change_group_role_keyboard

teachers_change_group_role_keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
teachers_change_group_role_keyboard.add(change_only_role_button)
teachers_change_group_role_keyboard.add(back_button)

student_changes_role_keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
student_changes_role_keyboard.add(teacher_button)
student_changes_role_keyboard.add(back_button)

teacher_changes_role_keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
teacher_changes_role_keyboard.add(student_button)
teacher_changes_role_keyboard.add(back_button)

re_register_keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
re_register_keyboard.add(student_button, teacher_button)
re_register_keyboard.add(back_button)

settings_keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
settings_keyboard.add(add_link_button, add_hotline_button, add_mail_button)
settings_keyboard.add(notifications_button, change_group_role_button)
settings_keyboard.add(back_button)

main_menu_keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
main_menu_keyboard.add(schedule_button, links_button)
main_menu_keyboard.add(hotlines_button, info_button, mails_button)
main_menu_keyboard.add(settings_button, help_button)

schedule_choose_keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
schedule_choose_keyboard.add(session_button)
schedule_choose_keyboard.add(today_day_button, tomorrow_day_button)
schedule_choose_keyboard.add(week1_button, week2_button)
schedule_choose_keyboard.add(back_button)

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
                                              KEYBOARD SECTION ENDING
########################################################################################################################                               
'''

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
        bot.register_next_step_handler(message, callback=start_message)


@bot.message_handler(content_types=['text'])
def registration(message):
    try:

        if message.text == student_button:
            bot.send_message(message.chat.id,
                             'Привет, трудяга! Чтобы показать расписание, мне нужно узнать твою группу 🙂',
                             reply_markup=back_button_keyboard)
            bot.register_next_step_handler(message, callback=student_registration)

        elif message.text == teacher_button:

            bot.send_message(message.chat.id,
                             'Добрый день! Чтобы показать Ваше расписание, мне нужно узнать Ваше полное имя, фамилию и отчество украинском 🙂',
                             reply_markup=back_button_keyboard)
            bot.register_next_step_handler(message, callback=teacher_registration)

        else:
            bot.send_message(message.chat.id, 'Не могу вас идентифицировать. Попробуйте еще раз',
                             reply_markup=role_choose_keyboard)
            bot.register_next_step_handler(message, callback=registration)




    except AttributeError:
        bot.send_message(message.chat.id, 'i dont understand, sorry bro', reply_markup=settings_keyboard)
        bot.register_next_step_handler(message, callback=settings)


@bot.message_handler(content_types=['text'])
def teacher_registration(message):
    try:

        if message.text == back_button:
            bot.send_message(message.chat.id, 'Возвращаемся назад...', reply_markup=role_choose_keyboard)
            bot.register_next_step_handler(message, callback=registration)

        else:
            if sch.is_teacher_exist(message.text):
                sch.identify_as('преподаватель', message.text)
                db.add_user(message.chat.id, sch.role, message.text)
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

                db.add_user(message.chat.id, sch.role, message.text)

                bot.send_message(message.chat.id, 'Есть такая! Ну а теперь приступим 🙂',
                                 reply_markup=main_menu_keyboard)
                bot.register_next_step_handler(message, callback=main_menu)

            else:
                bot.send_message(message.chat.id, '''Ой, что-то я о такой группе не слышал 🤥\nПоробуй ещё''')
                bot.register_next_step_handler(message, callback=student_registration)

    except AttributeError:
        bot.send_message(message.chat.id, 'Такие данные мне подходят 🙂')
        bot.register_next_step_handler(message, callback=student_registration)


'''                        
########################################################################################################################                    
                                                 MAIN MENU TREE       
########################################################################################################################                                                       
'''


@bot.message_handler(content_types=['text'])
def main_menu(message):
    info_message = "————— <b>Z-Moves Bot</b> —————\n\n" + \
                   "Бот создан с целью уведомлять пользователей по поводу расписания.\n\n" + \
                   "Вы авторизованы как: " + sch.role + ", " + (
                       sch.id.upper() if sch.id == 'студент' else sch.id) + "\n\n" + \
                   "Авторы:\nDanon(@danilos0)\nДимасик(@KickYourSelff)\nРостянский(@leap_sunrise)"

    help_message = "<b>Что может бот ?</b>\n\n" + \
                   "Пользователь может авторизоваться как студент или преподаватель.\n\n" + \
                   "Потом пользователь попадает в главное меню, где он может узнать:\n\n" + \
                   "-📆 Расписание сессии (Расписание ваших экзаменов)\n\n" + \
                   "-📝 Текущее расписание (Расписание на этот день, но не забывайте про выходные)\n\n" + \
                   "-📝 Расписание на завтра (Расписание на завтрашний день, если это не выходной)\n\n" + \
                   "-📆 Расписание (Расписание на целую неделю (На первую или вторую))\n\n" + \
                   "-⚙ Настройки (Отключение уведомлений, дедлайны, возможность перерегистрации, отключение уведомлений от бота)\n\n" + \
                   "-ℹ Инфо (Общая информация)\n\n" + \
                   "-❓ Помощь (Я есть грут)\n"
    try:
        if message.text == schedule_button:
            bot.send_message(message.chat.id, 'Выбери опцию отображения расписания', reply_markup=schedule_choose_keyboard)
            bot.register_next_step_handler(message, callback=schedule_choose)

        elif message.text == settings_button:
            bot.send_message(message.chat.id, 'Что ты желаешь настроить?', reply_markup=settings_keyboard)
            bot.register_next_step_handler(message, callback=settings)

        elif message.text == links_button:
            bot.send_message(message.chat.id, '————— 🔗 Links —————\n\n' + get_links(message.chat.id),
                             parse_mode='HTML',
                             disable_web_page_preview=True,
                             reply_markup=main_menu_keyboard)
            bot.register_next_step_handler(message, callback=main_menu)

        elif message.text == hotlines_button:
            hotlines = '————— 👺 Hotlines —————\n\n' + get_hotlines(message.chat.id)
            bot.send_message(message.chat.id, hotlines,
                             parse_mode='HTML',
                             disable_web_page_preview=True,
                             reply_markup=main_menu_keyboard)
            bot.register_next_step_handler(message, callback=main_menu)

        elif message.text == info_button:
            bot.send_message(message.chat.id, info_message, parse_mode='HTML', reply_markup=main_menu_keyboard)
            bot.register_next_step_handler(message, callback=main_menu)

        elif message.text == help_button:
            bot.send_message(message.chat.id, help_message, parse_mode='HTML', reply_markup=main_menu_keyboard)
            bot.register_next_step_handler(message, callback=main_menu)

        else:
            bot.send_message(message.chat.id, 'i dont understand, sorry bro', reply_markup=main_menu_keyboard)
            bot.register_next_step_handler(message, callback=main_menu)
    except AttributeError:
        bot.send_message(message.chat.id, 'i dont understand, sorry bro', reply_markup=settings_keyboard)
        bot.register_next_step_handler(message, callback=settings)


'''                        
########################################################################################################################                    
                                                 MAIN MENU TREE END
########################################################################################################################                                                       
'''

'''
########################################################################################################################                                            
                                                  SCHEDULE BRANCH BEGINNING               
########################################################################################################################                                                  
'''


def show_day(user_id: int, wd: str, day: int):
    if day > 5:
        s = wd + ' пар нету. Отдыхаем'
    else:
        weekday = week_days[day]
        cur_week = get_current_week()
        s = show_schedule(user_id, weekday, sch.get_schedule(cur_week, day))
    return s


@bot.message_handler(content_types=['text'])
def schedule_choose(message):
    try:
        if message.text == session_button:
            if session_tokens.__contains__(sch.id):
                bot.send_message(message.chat.id, sch.get_session_for_schedule(), parse_mode='HTML',
                                 reply_markup=schedule_choose_keyboard)
                bot.register_next_step_handler(message, callback=schedule_choose)
            else:
                bot.send_message(message.chat.id,
                                 develop_button + \
                                 '. \nНа данном этапе расписание сессии отображается только для групп і(о|в)-8X',
                                 reply_markup=schedule_choose_keyboard)
                bot.register_next_step_handler(message, callback=schedule_choose)
        elif message.text == today_day_button:
            s = show_day(message.chat.id, "Сегодня", date.today().weekday() + 1)
            bot.send_message(message.chat.id, s, parse_mode="HTML", reply_markup=schedule_choose_keyboard)
            bot.register_next_step_handler(message, callback=schedule_choose)
        elif message.text == tomorrow_day_button:
            tomorrow = (date.today() + datetime.timedelta(days=1)).weekday() + 1
            s = show_day(message.chat.id, "Завтра", tomorrow)
            bot.send_message(message.chat.id, s, parse_mode="HTML", reply_markup=schedule_choose_keyboard)
            bot.register_next_step_handler(message, callback=schedule_choose)
        elif message.text == week1_button:
            bot.send_message(message.chat.id, 'А теперь день', reply_markup=day_choose_keyboard)
            bot.register_next_step_handler(message, callback=week_1)
        elif message.text == week2_button:
            bot.send_message(message.chat.id, 'А теперь день', reply_markup=day_choose_keyboard)
            bot.register_next_step_handler(message, callback=week_2)
        elif message.text == back_button:
            bot.send_message(message.chat.id, 'Возвращаемся...', reply_markup=main_menu_keyboard)
            bot.register_next_step_handler(message, callback=main_menu)
        else:
            bot.send_message(message.chat.id, 'i dont understand, sorry bro', reply_markup=schedule_choose_keyboard)
            bot.register_next_step_handler(message, callback=schedule_choose)

    except AttributeError:
        bot.send_message(message.chat.id, 'i dont understand, sorry bro', reply_markup=settings_keyboard)
        bot.register_next_step_handler(message, callback=settings)


@bot.message_handler(content_types=['text'])
def week_1(message):
    try:
        if message.text == day_button[0]:
            bot.send_message(message.chat.id, show_schedule(message.chat.id, "понедельник", sch.get_schedule(1, 1)),
                             parse_mode="HTML",
                             reply_markup=day_choose_keyboard)
            bot.register_next_step_handler(message, callback=week_1)
        elif message.text == day_button[1]:
            bot.send_message(message.chat.id, show_schedule(message.chat.id, "вторник", sch.get_schedule(1, 2)),
                             parse_mode="HTML", reply_markup=day_choose_keyboard)
            bot.register_next_step_handler(message, callback=week_1)
        elif message.text == day_button[2]:
            bot.send_message(message.chat.id, show_schedule(message.chat.id, "среду", sch.get_schedule(1, 3)),
                             parse_mode="HTML", reply_markup=day_choose_keyboard)
            bot.register_next_step_handler(message, callback=week_1)
        elif message.text == day_button[3]:
            bot.send_message(message.chat.id, show_schedule(message.chat.id, "четверг", sch.get_schedule(1, 4)),
                             parse_mode="HTML",
                             reply_markup=day_choose_keyboard)
            bot.register_next_step_handler(message, callback=week_1)
        elif message.text == day_button[4]:
            bot.send_message(
                message.chat.id, show_schedule(message.chat.id, "пятницу", sch.get_schedule(1, 5)),
                parse_mode="HTML",
                reply_markup=day_choose_keyboard
            )
            bot.register_next_step_handler(message, callback=week_1)
        elif message.text == back_button:
            bot.send_message(message.chat.id, text='Возвращаемся назад...', reply_markup=schedule_choose_keyboard)
            bot.register_next_step_handler(message, callback=schedule_choose)
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
            bot.send_message(message.chat.id, show_schedule(message.chat.id, "понедельник", sch.get_schedule(2, 1)),
                             parse_mode="HTML", reply_markup=day_choose_keyboard)
            bot.register_next_step_handler(message, callback=week_2)
        elif message.text == day_button[1]:
            bot.send_message(message.chat.id, show_schedule(message.chat.id, "вторник", sch.get_schedule(2, 2)),
                             parse_mode="HTML", reply_markup=day_choose_keyboard)
            bot.register_next_step_handler(message, callback=week_2)
        elif message.text == day_button[2]:
            bot.send_message(message.chat.id, show_schedule(message.chat.id, "среду", sch.get_schedule(2, 3)),
                             parse_mode="HTML", reply_markup=day_choose_keyboard)
            bot.register_next_step_handler(message, callback=week_2)
        elif message.text == day_button[3]:
            bot.send_message(message.chat.id, show_schedule(message.chat.id, "четверг", sch.get_schedule(2, 4)),
                             parse_mode="HTML", reply_markup=day_choose_keyboard)
            bot.register_next_step_handler(message, callback=week_2)
        elif message.text == day_button[4]:
            bot.send_message(message.chat.id, show_schedule(message.chat.id, "пятницу", sch.get_schedule(2, 5)),
                             parse_mode="HTML", reply_markup=day_choose_keyboard)
            bot.register_next_step_handler(message, callback=week_2)
        elif message.text == back_button:
            bot.send_message(message.chat.id, text='Возвращаемся назад...', reply_markup=schedule_choose_keyboard)
            bot.register_next_step_handler(message, callback=schedule_choose)
        else:
            bot.send_message(message.chat.id, 'i dont understand, sorry bro', reply_markup=day_choose_keyboard)
            bot.register_next_step_handler(message, callback=week_2)

    except AttributeError:
        bot.send_message(message.chat.id, 'i dont understand, sorry bro', reply_markup=settings_keyboard)
        bot.register_next_step_handler(message, callback=settings)


'''
########################################################################################################################
                                             SCHEDULE BRANCH END         
########################################################################################################################
'''

'''                                            
########################################################################################################################
                                                  SETTINGS BRANCH BEGINNING
########################################################################################################################                                                                 
'''


@bot.message_handler(content_types=['text'])
def settings(message):
    try:
        if message.text == add_link_button:
            bot.send_message(message.chat.id,
                             '''
                             Введите ссылку в следующем формате:
                             <pre>Ссылка|Формат</pre>
                             ''',
                             parse_mode='HTML',
                             reply_markup=back_button_keyboard)
            bot.register_next_step_handler(message, adding_link)

        elif message.text == add_mail_button:
            bot.send_message(message.chat.id, '''Введите некст форматъ плес: ССЫЛКА|ДЕСКРИПШН''', parse_mode='HTML', reply_markup=back_button_keyboard)
            bot.register_next_step_handler(message, adding_mail)

        elif message.text == add_hotline_button:
            bot.send_message(message.chat.id,
                             'Для добавления хотлайна, тебе стоит прописать дедлайн в слудующем формате:\n\n' + \
                             '<pre>Название предмета|Описание работы|Срок выполнения|Ссылка(опционально)</pre>',
                             parse_mode='HTML',
                             reply_markup=back_button_keyboard)
            bot.register_next_step_handler(message, callback=adding_hotline)

        elif message.text == notifications_button:
            bot.send_message(message.chat.id, 'Введите время (в формате HH:MM), в которое я пришлю уведомление',
                             reply_markup=back_button_keyboard)
            bot.register_next_step_handler(message, callback=set_notification)

        elif message.text == change_group_role_button:

            if sch.role == 'студент':
                bot.send_message(message.chat.id, 'Меняй роль или группу.',
                                 reply_markup=student_change_group_role_keyboard)
                bot.register_next_step_handler(message, callback=change_role_group)

            elif sch.role == 'преподаватель':
                bot.send_message(message.chat.id, 'Меняй роль.',
                                 reply_markup=teachers_change_group_role_keyboard)
                bot.register_next_step_handler(message, callback=change_role_group)

        elif message.text == back_button:
            bot.send_message(message.chat.id, 'Возвращаемся...', reply_markup=main_menu_keyboard)
            bot.register_next_step_handler(message, callback=main_menu)

        else:
            bot.send_message(message.chat.id, 'i dont understand, sorry bro', reply_markup=settings_keyboard)
            bot.register_next_step_handler(message, callback=settings)

    except AttributeError:
        bot.send_message(message.chat.id, 'i dont understand, sorry bro', reply_markup=settings_keyboard)
        bot.register_next_step_handler(message, callback=settings)


'''                                            
########################################################################################################################
                                                  SETTINGS BRANCH END
########################################################################################################################                                                                 
'''

'''                                            
########################################################################################################################
                                                  NOTIFICATION PROCESS BEGINNING
########################################################################################################################                                                                 
'''

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
            bot.send_message(message.chat.id, 'Возвращаемся назад...', reply_markup=settings_keyboard)
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
    bot.send_message(message.chat.id, show_day(message.chat.id, "Завтра", date.today().weekday() + 1), parse_mode="HTML")
    global is_notification_on
    is_notification_on = False


notification_thread = Thread(target=schedule_checker)
notification_thread.start()

'''                                            
########################################################################################################################
                                                  NOTIFICATION PROCESS END
########################################################################################################################                                                                 
'''

'''                                            
########################################################################################################################
                                                  LINKS PROCESS BEGINNING
########################################################################################################################                                                                 
'''

@bot.message_handler(content_types=['text'])
def adding_link(message):
    try:
        if message.text == back_button:
            bot.send_message(message.chat.id, 'Возвращаемся назад...', reply_markup=settings_keyboard)
            bot.register_next_step_handler(message, callback=settings)
        else:
            links = message.text.split('|')
            if len(links) == 2:
                db.add_links(message.chat.id, links[0], links[1])
                bot.send_message(message.chat.id,
                                 'Ссылка была успешно добавлена. Теперь её можно найти, нажав на кнопку \'Ссылки\' в главном меню 🙂',
                                 reply_markup=settings_keyboard)
                bot.register_next_step_handler(message, callback=settings)
            else:
                bot.send_message(message.chat.id, 'Неверный формат для занесения ссылки. Попробуйте еще..', reply_markup=back_button_keyboard)
                bot.register_next_step_handler(message, callback=adding_link)
    except AttributeError:
        bot.send_message(message.chat.id, 'i dont understand, sorry bro', reply_markup=settings_keyboard)
        bot.register_next_step_handler(message, callback=settings)

'''
########################################################################################################################
                                                  LINKS PROCESS END
########################################################################################################################
'''

'''                                            
########################################################################################################################
                                                    HOTLINES BEGINNING
########################################################################################################################                                                                 
'''


@bot.message_handler(content_types=['text'])
def adding_hotline(message):
    try:
        if message.text == back_button:
            bot.send_message(message.chat.id, 'Возвращаемся назад...', reply_markup=settings_keyboard)
            bot.register_next_step_handler(message, callback=settings)
        else:
            hotlines = message.text.split('|')
            if len(hotlines) == 3:
                db.add_hotline_without_link(message.chat.id, hotlines[0], hotlines[1], hotlines[2])
                bot.send_message(message.chat.id,
                                 'Хотлайн был успешно добавлен. Теперь его можно будет наблюдать в вашем расписание 🙂',
                                 reply_markup=settings_keyboard)
                bot.register_next_step_handler(message, callback=settings)

            elif len(hotlines) == 4:
                db.add_hotline(message.chat.id, hotlines[0], hotlines[1], hotlines[2], hotlines[3])
                bot.send_message(message.chat.id,
                                 'Хотлайн был успешно добавлен. Теперь его можно будет наблюдать в вашем расписание 🙂',
                                 reply_markup=settings_keyboard)
                bot.register_next_step_handler(message, callback=settings)
            else:
                bot.send_message(message.chat.id, 'Неверный формат для занесения хотлайна. Попробуйте еще..', reply_markup=back_button_keyboard)
                bot.register_next_step_handler(message, callback=adding_hotline)
    except AttributeError:
        bot.send_message(message.chat.id, 'i dont understand, sorry bro', reply_markup=settings_keyboard)
        bot.register_next_step_handler(message, callback=settings)

'''
########################################################################################################################
                                                    HOTLINES END
########################################################################################################################
'''

'''
########################################################################################################################
                                                    MAILS BEGINNING
########################################################################################################################
'''

@bot.message_handler(content_types=['text'])
def adding_mail(message):
    try:

        if message.text == back_button:
            bot.send_message(message.chat.id, 'Возвращаемся назад...', reply_markup=settings_keyboard)
            bot.register_next_step_handler(message, callback=settings)

        else:
            mail = message.text.split('|')
            if len(mail) == 2:
                db.add_mail(message.chat.id, mail[0], mail[1])
                bot.send_message(message.chat.id, 'почта добавлена успешно! заебись! чётка!', reply_markup=settings_keyboard)
                bot.register_next_step_handler(message, callback=settings)

            else:
                bot.send_message(message.chat.id, 'Неверный формат для занесения хотлайна. Попробуйте еще..', reply_markup=back_button_keyboard)
                bot.register_next_step_handler(message, callback=adding_mail)

    except AttributeError:
        bot.send_message(message.chat.id, 'i dont understand, sorry bro', reply_markup=settings_keyboard)
        bot.register_next_step_handler(message, callback=settings)


'''
########################################################################################################################
                                                    MAILS ENDING
########################################################################################################################
'''

'''
########################################################################################################################
                                        CHANGE ROLE/GROUP PROCESS BEGINNING
########################################################################################################################                                                                 
'''


@bot.message_handler(content_types=['text'])
def change_role_group(message):
    try:
        if sch.role == 'студент':
            if message.text == change_only_group_button:
                bot.send_message(message.chat.id, 'Введи название группы', reply_markup=back_button_keyboard)
                bot.register_next_step_handler(message, callback=group_re_registration)

            elif message.text == change_only_role_button:
                bot.send_message(message.chat.id, 'Выбери роль', reply_markup=student_changes_role_keyboard)
                bot.register_next_step_handler(message, callback=role_re_registration)

            elif message.text == back_button:
                bot.send_message(message.chat.id, 'Мувимся назад', reply_markup=settings_keyboard)
                bot.register_next_step_handler(message, callback=settings)

        elif sch.role == 'преподаватель':

            if message.text == change_only_role_button:
                bot.send_message(message.chat.id, 'Выберите роль', reply_markup=teacher_changes_role_keyboard)
                bot.register_next_step_handler(message, callback=role_re_registration)

            elif message.text == back_button:
                bot.send_message(message.chat.id, 'Мувимся назад', reply_markup=settings_keyboard)
                bot.register_next_step_handler(message, callback=settings)

        else:
            bot.send_message(message.chat.id, 'i dont understand, sorry bro', reply_markup=settings_keyboard)
            bot.register_next_step_handler(message, callback=settings)

    except AttributeError:
        bot.send_message(message.chat.id, 'i dont understand, sorry bro', reply_markup=settings_keyboard)
        bot.register_next_step_handler(message, callback=settings)


@bot.message_handler(content_types=['text'])
def group_re_registration(message):
    try:
        if sch.role == 'студент':

            if sch.is_group_exist(message.text):
                sch.identify_as('студент', message.text)

                db.update_user(message.chat.id, sch.role, message.text)

                bot.send_message(message.chat.id, 'Есть такая ^_^', reply_markup=settings_keyboard)
                bot.register_next_step_handler(message, callback=settings)

            elif message.text == back_button:
                bot.send_message(message.chat.id, 'Возвращаюсь назад...', reply_markup=student_change_group_role_keyboard)
                bot.register_next_step_handler(message, callback=change_role_group)

        else:
            bot.send_message(message.chat.id, 'i dont understand, sorry bro', reply_markup=change_group_role_keyboard)
            bot.register_next_step_handler(message, callback=change_role_group)

    except AttributeError:
        bot.send_message(message.chat.id, 'i dont understand, sorry bro', reply_markup=settings_keyboard)
        bot.register_next_step_handler(message, callback=settings)


@bot.message_handler(content_types=['text'])
def role_re_registration(message):
    try:
        if sch.role == 'студент':
            if message.text == teacher_button:
                bot.send_message(message.chat.id, 'Введите ваше ФИО (на украинском)', reply_markup=back_button_keyboard)
                bot.register_next_step_handler(message, callback=teacher_re_identification)

            elif message.text == back_button:
                bot.send_message(message.chat.id, 'Возвращаюсь назад...', reply_markup=student_change_group_role_keyboard)
                bot.register_next_step_handler(message, callback=change_role_group)

            else:
                bot.send_message(message.chat.id, 'i dont understand, sorry bro',
                                 reply_markup=student_change_group_role_keyboard)
                bot.register_next_step_handler(message, callback=change_role_group)

        elif sch.role == 'преподаватель':

            if message.text == student_button:
                bot.send_message(message.chat.id, 'Введите название группы', reply_markup=back_button_keyboard)
                bot.register_next_step_handler(message, callback=teacher_re_identification)

            elif message.text == back_button:
                bot.send_message(message.chat.id, 'Возвращаюсь назад...', reply_markup=teachers_change_group_role_keyboard)
                bot.register_next_step_handler(message, callback=change_role_group)

    except AttributeError:
        bot.send_message(message.chat.id, 'i dont understand, sorry bro', reply_markup=settings_keyboard)
        bot.register_next_step_handler(message, callback=settings)


@bot.message_handler(content_types=['text'])
def teacher_re_identification(message):
    try:
        if sch.role == 'студент':

            if sch.is_teacher_exist(message.text):
                sch.identify_as('преподаватель', message.text)
                db.update_user(message.chat.id, sch.role, message.text)
                bot.send_message(message.chat.id, 'Добрый день, {0}!'.format(sch.get_teacher_name(message.text)),
                                 reply_markup=main_menu_keyboard)
                bot.register_next_step_handler(message, callback=main_menu)

            elif message.text == back_button:
                bot.send_message(message.chat.id, 'Возвращаюсь назад...', reply_markup=student_changes_role_keyboard)
                bot.register_next_step_handler(message, callback=role_re_registration)

            else:
                bot.send_message(message.chat.id, 'i dont understand, sorry bro',
                                 reply_markup=change_group_role_keyboard)
                bot.register_next_step_handler(message, callback=change_role_group)

        elif sch.role == 'преподаватель':

            if sch.is_group_exist(message.text):
                sch.identify_as('студент', message.text)
                db.update_user(message.chat.id, sch.role, message.text)
                bot.send_message(message.chat.id, 'Есть такая ^_^', reply_markup=settings_keyboard)
                bot.register_next_step_handler(message, callback=settings)

            elif message.text == back_button:
                bot.send_message(message.chat.id, 'Возвращаюсь назад...', reply_markup=teacher_changes_role_keyboard)
                bot.register_next_step_handler(message, callback=role_re_registration)

    except AttributeError:
        bot.send_message(message.chat.id, 'i dont understand, sorry bro', reply_markup=settings_keyboard)
        bot.register_next_step_handler(message, callback=settings)


'''                                            
########################################################################################################################
                                        CHANGE ROLE/GROUP PROCESS BEGINNING
########################################################################################################################                                                                 
'''

if __name__ == '__main__':
    bot.polling()
