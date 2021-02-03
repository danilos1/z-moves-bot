import datetime
import os
import time
from z_moves.buttons import *
from z_moves.scripts.schedule_parser import *
from z_moves.scripts import db
import z_moves.scripts.service.links as links
import z_moves.scripts.service.users as users

bot = telebot.TeleBot(os.environ['BOT_TOKEN'])
db.init_db()

'''
########################################################################################################################
KEYBOARD SECTION
########################################################################################################################                               
'''

# main menu
main_menu_keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
main_menu_keyboard.add(schedule_button, settings_button)
main_menu_keyboard.add(links_button, hotlines_button, mails_button)
main_menu_keyboard.add(info_button, help_button)
main_menu_keyboard.add(test_button)

links_inline_ready_keyboard = telebot.types.InlineKeyboardMarkup()
links_inline_ready_keyboard.add(links_inline_ready_button)


links_subject_type_inline_keyboard = telebot.types.InlineKeyboardMarkup()
links_subject_type_inline_keyboard.add(links_inline_lec_button, links_inline_lab_button, links_inline_practice_button)
links_subject_type_inline_keyboard.add(telebot.types.InlineKeyboardButton(text='Назад', callback_data='second_back_button'), in_main_menu_inline_button)

test_keyboard = telebot.types.InlineKeyboardMarkup()
test_keyboard.add(test_button)

# schedule menu keyboard
schedule_menu_keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
schedule_menu_keyboard.add(today_day_button, tomorrow_day_button)
schedule_menu_keyboard.add(week1_button, week2_button)
schedule_menu_keyboard.add(back_button)

# schedule menu (day choosing) keyboard
week1_day_choose_keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
week1_day_choose_keyboard.add(week1_day_buttons[0], week1_day_buttons[1], week1_day_buttons[2])
week1_day_choose_keyboard.add(week1_day_buttons[3], week1_day_buttons[4])
week1_day_choose_keyboard.add(back_button)

week2_day_choose_keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
week2_day_choose_keyboard.add(week2_day_buttons[0], week2_day_buttons[1], week2_day_buttons[2])
week2_day_choose_keyboard.add(week2_day_buttons[3], week2_day_buttons[4])
week2_day_choose_keyboard.add(back_button)

# settings menu keyboard
settings_menu_keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
settings_menu_keyboard.add(add_link_button, add_hotline_button, add_mail_button)
settings_menu_keyboard.add(notification_button, change_group_name_button)
settings_menu_keyboard.add(back_button)

# global back button keyboard
back_button_keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
back_button_keyboard.add(back_button)

'''
########################################################################################################################
KEYBOARD SECTION END
########################################################################################################################                               
'''

'''
########################################################################################################################
REGISTRATION
########################################################################################################################
'''

@bot.message_handler(commands=['start'])
def start_message(message):
    try:
        user_first_name = message.from_user.first_name
        user_last_name = ''
        if message.from_user.last_name is not None:
            user_last_name = ' ' + message.from_user.last_name

        bot.send_message(message.chat.id, 'Привет, {}{}! 🥴🤙\nZ-Moves на связи 😎\n\nДля работы со мной напиши мне '
                                          'название своей группы.\n\nПример: <b>IO-83</b>'.
                         format(user_first_name, user_last_name), parse_mode='HTML')
        bot.register_next_step_handler(message, callback=registration)

    except AttributeError:
        bot.send_message(message.chat.id, 'i dont understand, sorry bro')
        bot.register_next_step_handler(message, callback=start_message)

@bot.message_handler(content_types=['text'])
def registration(message):
    try:
        if Schedule.is_group_exist(message.text):
            if users.is_user_exists(message.chat.id):
                users.update_user(message.chat.id, message.text.upper())
            else:
                users.add_user(message.chat.id, message.from_user.username, message.text.upper())

            bot.send_message(message.chat.id, 'Есть такая! Ну а теперь приступим 🙂',
                             reply_markup=main_menu_keyboard)
            bot.register_next_step_handler(message, main_menu)

            global links_inline_subjects_keyboard, w, w_dict
            links_inline_subjects_keyboard = telebot.types.InlineKeyboardMarkup()

            w = []
            w_dict = {}

            list_subjects = list(Schedule.get_lessons(message.chat.id))
            len_list_subjects = len(Schedule.get_lessons(message.chat.id))
            len_subjects = 0
            for subject in list_subjects:
                len_subjects += 1
                w.append(subject)
                w_dict[subject[:15]] = subject

                if len_subjects < len_list_subjects + 1:
                    links_inline_subjects_keyboard.add(
                        telebot.types.InlineKeyboardButton(text=subject, callback_data='{}'.format(subject[:15])))
            links_inline_subjects_keyboard.add(
                 telebot.types.InlineKeyboardButton(text='Назад', callback_data='first_back_button'), in_main_menu_inline_button)
            bot.register_next_step_handler(message, callback=main_menu)


        else:
            bot.send_message(message.chat.id, '<b>{}</b>? Что-то я о такой группе ещё не слышал 🤥'
                                              'Попробуй ещё.'.format(message.text), parse_mode='HTML')
            bot.register_next_step_handler(message, callback=registration)

    except AttributeError:
        bot.send_message(message.chat.id, 'i dont understand, sorry bro')
        bot.register_next_step_handler(message, callback=registration)


'''
########################################################################################################################
REGISTRATION END
########################################################################################################################
'''

'''                        
########################################################################################################################                    
MAIN MENU  
########################################################################################################################                                                       
'''


@bot.message_handler(content_types=['text'])
def main_menu(message):
    try:
        if message.text == schedule_button:
            db.users_update_last_activity(message.from_user.username, time.strftime('%d/%m/%y, %X'), message.chat.id)
            bot.send_message(message.chat.id, 'Выбери опцию отображения расписания.',
                             reply_markup=schedule_menu_keyboard)
            bot.register_next_step_handler(message, callback=schedule_menu)

        elif message.text == settings_button:
            db.users_update_last_activity(message.from_user.username, time.strftime('%d/%m/%y, %X'), message.chat.id)
            bot.send_message(message.chat.id, 'Что ты желаешь настроить?', reply_markup=settings_menu_keyboard)
            bot.register_next_step_handler(message, callback=settings_menu)

        elif message.text == links_button:
            link_inline_keyboard = telebot.types.InlineKeyboardMarkup()
            link_inline_keyboard.add(links_inline_add_button)
            link_inline_keyboard.add(in_main_menu_inline_button)
            db.users_update_last_activity(message.from_user.username, time.strftime('%d/%m/%y, %X'), message.chat.id)
            bot.send_message(message.chat.id,
                             links.get_links(message.chat.id),
                             parse_mode='HTML',
                             reply_markup=link_inline_keyboard)

        elif message.text == hotlines_button:
            db.users_update_last_activity(message.from_user.username, time.strftime('%d/%m/%y, %X'), message.chat.id)
            bot.send_message(message.chat.id, '————— 👺 Hotlines —————\n\n' + get_hotlines(message.chat.id),
                             parse_mode='HTML', disable_web_page_preview=True, reply_markup=main_menu_keyboard)
            bot.register_next_step_handler(message, callback=main_menu)

        elif message.text == mails_button:
            db.users_update_last_activity(message.from_user.username, time.strftime('%d/%m/%y, %X'), message.chat.id)
            bot.send_message(message.chat.id, '————— 🔗 MAILS —————\n\n' + get_mails(message.chat.id),
                             parse_mode='HTML', disable_web_page_preview=True, reply_markup=main_menu_keyboard)
            bot.register_next_step_handler(message, callback=main_menu)

        elif message.text == info_button:
            db.users_update_last_activity(message.from_user.username, time.strftime('%d/%m/%y, %X'), message.chat.id)
            bot.send_message(message.chat.id, info_button_reply.format(db.get_group_name_by_id(message.chat.id)[0]),
                             parse_mode='HTML', reply_markup=main_menu_keyboard)
            bot.register_next_step_handler(message, callback=main_menu)

        elif message.text == help_button:
            db.users_update_last_activity(message.from_user.username, time.strftime('%d/%m/%y, %X'), message.chat.id)
            bot.send_message(message.chat.id, help_button_reply, parse_mode='HTML', reply_markup=main_menu_keyboard)
            bot.register_next_step_handler(message, callback=main_menu)

        elif message.text == test_button:
            db.users_update_last_activity(message.from_user.username, time.strftime('%d/%m/%y, %X'), message.chat.id)
            bot.send_message(message.chat.id, not_available_reply, reply_markup=main_menu_keyboard)

        elif message.text == '/start':
            bot.send_message(message.chat.id, rereg_reply, reply_markup=None, parse_mode='HTML')
            bot.register_next_step_handler(message, registration)

        else:
            bot.send_message(message.chat.id, 'qwrqwr', reply_markup=main_menu_keyboard)
            bot.register_next_step_handler(message, main_menu)


    except AttributeError:

        bot.send_message(message.chat.id, 'i dont understand, sorry bro', reply_markup=None )
        bot.register_next_step_handler(message, callback=main_menu)


subject_link_var = None
subject_password_var = None

link_redact_keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
link_redact_keyboard.add('Добавить ссылку', 'Добавить пароль')
link_redact_keyboard.add('Отмена', 'Далее')

add_link_password_keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
add_link_password_keyboard.add(back_button, 'Готово')

cancel_or_confirm_keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
cancel_or_confirm_keyboard.add('Отмена', 'Готово')

in_main_menu_keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
in_main_menu_keyboard.add(in_main_menu_button)

cancel_keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
cancel_keyboard.add(cancel_button)

@bot.callback_query_handler(func=lambda call: True)
def test_inline_reply(call):
    global subject_var, subject_type_var, link_inline_keyboard, link_redact_keyboard

    if call.data == 'add_link':
        bot.edit_message_text(text='Выбери предмет', chat_id=call.message.chat.id,
                              message_id=call.message.message_id, reply_markup=links_inline_subjects_keyboard, parse_mode='HTML')

    elif call.data in w_dict.keys():
        bot.edit_message_text(text='Выбери тип занятия', chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=links_subject_type_inline_keyboard, parse_mode='HTML')
        subject_var = w_dict.get(call.data)

    elif call.data == 'first_back_button':
        bot.edit_message_text(text='Выбери предмет', chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=link_inline_keyboard, parse_mode='HTML')

    elif call.data == 'second_back_button':
        bot.edit_message_text(text='Выбери чёта', chat_id=call.message.chat.id, message_id=call.message.message_id,
                              reply_markup=links_inline_subjects_keyboard, parse_mode='HTML')

    elif call.data == 'Лаб' or call.data == 'Лек' or call.data == 'Прак':
        subject_type_var = call.data
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

        bot.send_message(call.message.chat.id, 'Вы выбрали предмет:\n<i>{}</i> — <b>{}</b>. \nЕБАШ ССЫЛКУ ИЛИ Я ТЯ ЗАХУЯРЮ'.format(subject_var, subject_type_var), reply_markup=cancel_keyboard, parse_mode='HTML')
        bot.register_next_step_handler(call.message, input_link)

    elif call.data == 'main_menu':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, 'main menu', reply_markup=main_menu_keyboard)
        bot.register_next_step_handler(call.message, main_menu)


@bot.message_handler(content_types=['text'])
def input_link_menu(message):
    global subject_var, subject_type_var, subject_link_var, subject_password_var, link_redact_keyboard

    if message.text == 'Добавить ссылку' or message.text == 'Изменить cсылку':
        bot.send_message(message.chat.id, 'отправьте мне ссылку на пару', reply_markup=add_link_password_keyboard)
        bot.register_next_step_handler(message, input_link)

    elif message.text == 'Добавить пароль' or message.text == 'Изменить пароль':
        bot.send_message(message.chat.id, 'отправьте мне пароль к ссылке, если он присутствует', reply_markup=add_link_password_keyboard)
        bot.register_next_step_handler(message, input_link_pass)

    elif message.text == 'Отмена':
        bot.send_message(message.chat.id, 'Главное меню', reply_markup=main_menu_keyboard)
        bot.register_next_step_handler(message, main_menu)

    else:
        bot.send_message(message.chat.id, 'клас')
        bot.register_next_step_handler(message, input_link_menu)


@bot.message_handler(content_types=['text'])
def input_link(message):
    global subject_var, subject_type_var, subject_link_var, subject_password_var, link_redact_keyboard

    if message.text:

        if message.text == 'Отмена':
            bot.send_message(message.chat.id, 'Главное меню', reply_markup=main_menu_keyboard)
            bot.register_next_step_handler(message, main_menu)

        elif message.text == 'Готово':
            if subject_password_var is None:
                bot.send_message(message.chat.id, 'Вы успешно добавили ссылку.\nПредмет: {}-{}\nСсылка: {}'.format(subject_var, subject_type_var, subject_link_var), reply_markup=main_menu_keyboard)
                db.add_links(message.chat.id, subject_var, subject_type_var, subject_link_var)
                subject_link_var = None
                subject_password_var = None
                bot.register_next_step_handler(message, main_menu)
            elif subject_password_var is not None:
                bot.send_message(message.chat.id,
                                 'Вы успешно добавили ссылку.\nПредмет: {}-{}\nСсылка: {}\nПароль: {}'.format(subject_var,
                                                                                                  subject_type_var,
                                                                                                  subject_link_var, subject_password_var),
                                 reply_markup=main_menu_keyboard)
                db.add_links(message.chat.id, subject_var, subject_type_var, subject_link_var, subject_password_var)
                subject_link_var = None
                subject_password_var = None
                bot.register_next_step_handler(message, main_menu)

        elif message.text == 'Добавить пароль' or message.text == 'Изменить пароль':
            inserted_link_keyboard_to_password = telebot.types.ReplyKeyboardMarkup(True, True)
            inserted_link_keyboard_to_password.add('Изменить ссылку')
            inserted_link_keyboard_to_password.add(cancel_button, ready_button)
            bot.send_message(message.chat.id, 'Отправляй пароль гнида', reply_markup=inserted_link_keyboard_to_password)
            bot.register_next_step_handler(message, input_link_pass)

        elif message.text == message.text:
            if subject_password_var is None:
                subject_link_var = message.text
                inserted_link_keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
                inserted_link_keyboard.add('Добавить пароль')
                inserted_link_keyboard.add(cancel_button, ready_button)
                bot.send_message(message.chat.id, 'Предмет: {} - {}\nСсылка: {}\n\nТеперь можна крч подтверждать или добавить пароль, если надо'.format(subject_var, subject_type_var, subject_link_var), reply_markup=inserted_link_keyboard, disable_web_page_preview=True)
                bot.register_next_step_handler(message, input_link)
            elif subject_password_var is not None:
                subject_link_var = message.text
                inserted_link_keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
                inserted_link_keyboard.add('Изменить пароль')
                inserted_link_keyboard.add(cancel_button, ready_button)
                bot.send_message(message.chat.id,
                                 'Предмет: {} - {}\nСсылка: {}\nПароль: {}\n\nТеперь можна крч подтверждать или добавить пароль, если надо'.format(
                                     subject_var, subject_type_var, subject_link_var, subject_password_var), reply_markup=inserted_link_keyboard,
                                 disable_web_page_preview=True)
                bot.register_next_step_handler(message, input_link)

    else:
        bot.send_message(message.chat.id, 'клас')
        bot.register_next_step_handler(message, input_link)

@bot.message_handler(content_types=['text'])
def input_link_pass(message):
    global subject_link_var, subject_password_var, link_redact_keyboard, subject_var, subject_type_var

    if message.text == 'Готово':
        if subject_password_var is None:
            bot.send_message(message.chat.id, 'Вы успешно Предмет: {} - {}\nСсылка: {}\n'.format(subject_var, subject_type_var, subject_link_var), reply_markup=main_menu_keyboard, disable_web_page_preview=True)
            db.add_links(message.chat.id, subject_var, subject_type_var, subject_link_var, subject_password_var)
            subject_link_var = None
            subject_password_var = None
            bot.register_next_step_handler(message, main_menu)

        elif subject_password_var is not None:
            bot.send_message(message.chat.id, 'Заебись нахуй. Предмет: {} - {}\nСсылка: {}\nПароль: {}'.format(subject_var, subject_type_var, subject_link_var, subject_password_var), reply_markup=main_menu_keyboard, disable_web_page_preview=True)
            db.add_links(message.chat.id, subject_var, subject_type_var, subject_link_var, subject_password_var)
            subject_link_var = None
            subject_password_var = None
            bot.register_next_step_handler(message, main_menu)

    elif message.text == 'Изменить ссылку':
        if subject_password_var is not None:
            change_link_keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
            change_link_keyboard.add('Изменить пароль')
            change_link_keyboard.add(cancel_button, ready_button)
            bot.send_message(message.chat.id, 'якижи я заибавси памагити... \nПредмет: {} - {}\nСсылка: {}\nПароль: {}'.format(subject_var, subject_type_var, subject_link_var, subject_password_var), reply_markup=change_link_keyboard)
            bot.register_next_step_handler(message, input_link)
        elif subject_password_var is None:
            change_link_keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
            change_link_keyboard.add('Изменить пароль')
            change_link_keyboard.add(cancel_button, ready_button)
            bot.send_message(message.chat.id, 'якижи я заибавси памагити... \nПредмет: {} - {}\nСсылка: {}'.format(subject_var, subject_type_var, subject_link_var),reply_markup=change_link_keyboard)
            bot.register_next_step_handler(message, input_link)

    else:
        subject_password_var = message.text
        bot.send_message(message.chat.id,
                         'Предмет: {} - {}\nСсылка: {}\nПароль: {}'.format(subject_var, subject_type_var, subject_link_var, subject_password_var), disable_web_page_preview=True)
        bot.register_next_step_handler(message, input_link_pass)


'''                        
########################################################################################################################                    
MAIN MENU END
########################################################################################################################                                                       
'''

'''
########################################################################################################################                                            
SCHEDULE MENU            
########################################################################################################################                                                  
'''

@bot.message_handler(content_types=['text'])
def schedule_menu(message):
    try:
        if message.text == back_button:
            bot.send_message(message.chat.id, 'Возвращаемся...', reply_markup=main_menu_keyboard)
            bot.register_next_step_handler(message, callback=main_menu)

        elif message.text == today_day_button:
            s = show_day(message.chat.id, "Сегодня", date.today().weekday() + 1)
            bot.send_message(message.chat.id, s, parse_mode="HTML", reply_markup=schedule_menu_keyboard)
            bot.register_next_step_handler(message, callback=schedule_menu)

        elif message.text == tomorrow_day_button:
            tomorrow = (date.today() + datetime.timedelta(days=1)).weekday() + 1
            s = show_day(message.chat.id, "Завтра", tomorrow)
            bot.send_message(message.chat.id, s, parse_mode="HTML", reply_markup=schedule_menu_keyboard)
            bot.register_next_step_handler(message, callback=schedule_menu)

        elif message.text == week1_button:
            bot.send_message(message.chat.id, 'А теперь день', reply_markup=week1_day_choose_keyboard)
            bot.register_next_step_handler(message, callback=week_1)

        elif message.text == week2_button:
            bot.send_message(message.chat.id, 'А теперь день', reply_markup=week2_day_choose_keyboard)
            bot.register_next_step_handler(message, callback=week_2)


    except AttributeError:
        bot.send_message(message.chat.id, 'i dont understand, sorry bro', reply_markup=schedule_menu_keyboard)
        bot.register_next_step_handler(message, callback=schedule_menu)


@bot.message_handler(content_types=['text'])
def week_1(message):
    try:

        if message.text == week1_day_buttons[0]:
            bot.send_message(message.chat.id, Schedule.show_schedule(message.chat.id, 1, 1, "понедельник"),
                             parse_mode="HTML", reply_markup=week1_day_choose_keyboard)
            bot.register_next_step_handler(message, callback=week_1)

        elif message.text == week1_day_buttons[1]:
            bot.send_message(message.chat.id, Schedule.show_schedule(message.chat.id, 1, 2, "вторник"),
                             parse_mode="HTML", reply_markup=week1_day_choose_keyboard)
            bot.register_next_step_handler(message, callback=week_1)

        elif message.text == week1_day_buttons[2]:
            bot.send_message(message.chat.id, Schedule.show_schedule(message.chat.id, 1, 3, "среду"),
                             parse_mode="HTML", reply_markup=week1_day_choose_keyboard)
            bot.register_next_step_handler(message, callback=week_1)

        elif message.text == week1_day_buttons[3]:
            bot.send_message(message.chat.id,
                             Schedule.show_schedule(message.chat.id, 1, 4, "четверг"),
                             parse_mode="HTML",
                             reply_markup=week1_day_choose_keyboard)
            bot.register_next_step_handler(message, callback=week_1)

        elif message.text == week1_day_buttons[4]:
            bot.send_message(message.chat.id,
                             Schedule.show_schedule(message.chat.id, 1, 5, "пятницу"),
                             parse_mode="HTML",
                             reply_markup=week1_day_choose_keyboard)
            bot.register_next_step_handler(message, callback=week_1)

        elif message.text == back_button:
            bot.send_message(message.chat.id, text='Возвращаемся назад...', reply_markup=schedule_menu_keyboard)
            bot.register_next_step_handler(message, callback=schedule_menu)

        else:
            bot.send_message(message.chat.id, 'i dont understand, sorry bro', reply_markup=week1_day_choose_keyboard)
            bot.register_next_step_handler(message, callback=week_1)

    except AttributeError:
        bot.send_message(message.chat.id, 'i dont understand, sorry bro', reply_markup=week1_day_choose_keyboard)
        bot.register_next_step_handler(message, callback=week_1)


@bot.message_handler(content_types=['text'])
def week_2(message):
    try:

        if message.text == week2_day_buttons[0]:
            bot.send_message(message.chat.id,
                             Schedule.show_schedule(message.chat.id, 2, 1, "понедельник"),
                             parse_mode="HTML", reply_markup=week2_day_choose_keyboard)
            bot.register_next_step_handler(message, callback=week_2)

        elif message.text == week2_day_buttons[1]:
            bot.send_message(message.chat.id,
                             Schedule.show_schedule(message.chat.id, 2, 2, "вторник"),
                             parse_mode="HTML", reply_markup=week2_day_choose_keyboard)
            bot.register_next_step_handler(message, callback=week_2)

        elif message.text == week2_day_buttons[2]:
            bot.send_message(message.chat.id,
                             Schedule.show_schedule(message.chat.id, 2, 3, "среду"),
                             parse_mode="HTML", reply_markup=week2_day_choose_keyboard)
            bot.register_next_step_handler(message, callback=week_2)

        elif message.text == week2_day_buttons[3]:
            bot.send_message(message.chat.id,
                             Schedule.show_schedule(message.chat.id, 2, 4, "четверг"),
                             parse_mode="HTML", reply_markup=week2_day_choose_keyboard)
            bot.register_next_step_handler(message, callback=week_2)

        elif message.text == week2_day_buttons[4]:
            bot.send_message(message.chat.id,
                             Schedule.show_schedule(message.chat.id, 2, 5, "пятницу"),
                             parse_mode="HTML", reply_markup=week2_day_choose_keyboard)
            bot.register_next_step_handler(message, callback=week_2)

        elif message.text == back_button:
            bot.send_message(message.chat.id, text='Возвращаемся назад...', reply_markup=schedule_menu_keyboard)
            bot.register_next_step_handler(message, callback=schedule_menu)

        else:
            bot.send_message(message.chat.id, 'i dont understand, sorry bro', reply_markup=week2_day_choose_keyboard)
            bot.register_next_step_handler(message, callback=week_2)

    except AttributeError:
        bot.send_message(message.chat.id, 'i dont understand, sorry bro', reply_markup=week2_day_choose_keyboard)
        bot.register_next_step_handler(message, callback=week_2)


'''
########################################################################################################################
SCHEDULE MENU END       
########################################################################################################################
'''

'''                                            
########################################################################################################################
SETTINGS MENU
########################################################################################################################                                                                 
'''


@bot.message_handler(content_types=['text'])
def settings_menu(message):
    try:
        if message.text == back_button:
            bot.send_message(message.chat.id, 'Возвращаемся...', reply_markup=main_menu_keyboard)
            bot.register_next_step_handler(message, callback=main_menu)

        elif message.text == add_link_button:
            bot.send_message(message.chat.id, 'Введите ссылку в следующем формате: <pre>Ссылка|Формат</pre>',
                             parse_mode='HTML', reply_markup=back_button_keyboard)
            bot.register_next_step_handler(message, add_link)

        elif message.text == add_mail_button:
            bot.send_message(message.chat.id, '''Введите некст форматъ плес: ССЫЛКА|ДЕСКРИПШН''', parse_mode='HTML',
                             reply_markup=back_button_keyboard)
            bot.register_next_step_handler(message, add_mail)

        elif message.text == add_hotline_button:
            bot.send_message(message.chat.id,
                             'Для добавления хотлайна, тебе стоит прописать дедлайн в слудующем формате:\n\n'
                             '<pre>Название предмета, Описание работы, Срок выполнения, Ссылка(опционально)</pre>',
                             parse_mode='HTML', reply_markup=back_button_keyboard)
            bot.register_next_step_handler(message, callback=add_hotline)

        elif message.text == notification_button:
            bot.send_message(message.chat.id, not_available_reply, reply_markup=settings_menu_keyboard)
            bot.register_next_step_handler(message, callback=settings_menu)

        elif message.text == change_group_name_button:
            bot.send_message(message.chat.id, 'Введи название новой группы.\n'
                                              'Напоминаю, сейчас ты залогинен под группой: <b>{}</b>.'.
                             format(db.get_group_name_by_id(message.chat.id)[0].upper()), parse_mode='HTML',
                             reply_markup=back_button_keyboard)
            bot.register_next_step_handler(message, callback=change_group_name)

        else:
            bot.send_message(message.chat.id, 'i dont understand, sorry bro', reply_markup=settings_menu_keyboard)
            bot.register_next_step_handler(message, callback=settings_menu)

    except AttributeError:
        bot.send_message(message.chat.id, 'i dont understand, sorry bro', reply_markup=settings_menu_keyboard)
        bot.register_next_step_handler(message, callback=settings_menu)


'''                                            
########################################################################################################################
SETTINGS MENU END
########################################################################################################################                                                                 
'''

'''                                            
########################################################################################################################
LINK FUNCTION
########################################################################################################################                                                                 
'''


@bot.message_handler(content_types=['text'])
def add_link(message):
    try:
        if message.text == back_button:
            bot.send_message(message.chat.id, 'Возвращаемся назад...', reply_markup=settings_menu_keyboard)
            bot.register_next_step_handler(message, callback=settings_menu)

        else:
            links = message.text.split('|')
            if len(links) == 2:
                bot.send_message(message.chat.id,
                                 'Ссылка была успешно добавлена. Теперь её можно найти, нажав на кнопку'
                                 ' \'Ссылки\' в главном меню 🙂', reply_markup=settings_menu_keyboard)
                bot.register_next_step_handler(message, callback=settings_menu)

            else:
                bot.send_message(message.chat.id, 'Неверный формат для занесения ссылки. Попробуйте еще..',
                                 reply_markup=back_button_keyboard)
                bot.register_next_step_handler(message, callback=add_link)

    except AttributeError:
        bot.send_message(message.chat.id, 'i dont understand, sorry bro', reply_markup=back_button_keyboard)
        bot.register_next_step_handler(message, callback=add_link)


'''
########################################################################################################################
LINK FUNCTION END
########################################################################################################################
'''

'''                                            
########################################################################################################################
HOTLINE FUNCTION
########################################################################################################################                                                                 
'''


@bot.message_handler(content_types=['text'])
def add_hotline(message):
    try:
        if message.text == back_button:
            bot.send_message(message.chat.id, 'Возвращаемся назад...', reply_markup=settings_menu_keyboard)
            bot.register_next_step_handler(message, callback=settings_menu)

        else:
            hotlines = message.text.split(', ')

            if len(hotlines) == 3:
                db.add_hotline_without_link(message.chat.id, hotlines[0], hotlines[1], hotlines[2])
                bot.send_message(message.chat.id,
                                 'Хотлайн был успешно добавлен. Теперь его можно увидеть нажав на кнопочку {} в '
                                 'главном меню бота 🙂'.format(hotlines_button),
                                 reply_markup=settings_menu_keyboard)
                bot.register_next_step_handler(message, callback=settings_menu)

            elif len(hotlines) == 4:
                db.add_hotline_with_link(message.chat.id, hotlines[0], hotlines[1], hotlines[2], hotlines[3])
                bot.send_message(message.chat.id,
                                 'Хотлайн был успешно добавлен. Теперь его можно увидеть нажав на кнопочку {} в '
                                 'главном меню бота 🙂'.format(hotlines_button),
                                 reply_markup=settings_menu_keyboard)
                bot.register_next_step_handler(message, callback=settings_menu)

            else:
                bot.send_message(message.chat.id, 'Неверный формат для занесения хотлайна. Попробуйте еще..',
                                 reply_markup=back_button_keyboard)
                bot.register_next_step_handler(message, callback=add_hotline)

    except AttributeError:
        bot.send_message(message.chat.id, 'i dont understand, sorry bro', back_button_keyboard)
        bot.register_next_step_handler(message, callback=add_hotline)


'''
########################################################################################################################
HOTLINE FUNCTION END
########################################################################################################################
'''

'''
########################################################################################################################
MAIL FUNCTION
########################################################################################################################
'''


@bot.message_handler(content_types=['text'])
def add_mail(message):
    try:

        if message.text == back_button:
            bot.send_message(message.chat.id, 'Возвращаемся назад...', reply_markup=settings_menu_keyboard)
            bot.register_next_step_handler(message, callback=settings_menu)

        else:
            mails = message.text.split('|')

            if len(mails) == 2:
                db.add_mails(message.chat.id, mails[0], mails[1])
                bot.send_message(message.chat.id, 'почта добавлена успешно! заебись! чётка!',
                                 reply_markup=settings_menu_keyboard)
                bot.register_next_step_handler(message, callback=settings_menu)

            else:
                bot.send_message(message.chat.id, 'Неверный формат для занесения хотлайна. Попробуйте еще..',
                                 reply_markup=back_button_keyboard)
                bot.register_next_step_handler(message, callback=add_mail)

    except AttributeError:
        bot.send_message(message.chat.id, 'i dont understand, sorry bro', reply_markup=back_button_keyboard)
        bot.register_next_step_handler(message, callback=add_mail)


'''
########################################################################################################################
MAIL FUNCTION END
########################################################################################################################
'''

'''                                            
########################################################################################################################
NOTIFICATION FUNCTION
########################################################################################################################                                                                 
'''


@bot.message_handler(content_types=['text'])
def set_notification(message):
    try:

        if message.text == back_button:
            bot.send_message(message.chat.id, 'Возвращаемся назад...', reply_markup=settings_menu_keyboard)
            bot.register_next_step_handler(message, callback=settings_menu)

        # elif re.match("^(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$", message.text):
        #     cron_date = '{0} {1} * * *'.format(int(message.text[3::]), int(message.text[:2]))  # 12:23
        #     db.add_notification(message.chat.id, cron_date)
        #     send_notification(message.chat.id, cron_date)
        #     bot.send_message(message.chat.id, 'Время установлено', reply_markup=settings_menu_keyboard)
        #     bot.register_next_step_handler(message, callback=settings_menu)

        else:
            bot.send_message(message.chat.id, 'Немножечко не по формату :(', reply_markup=back_button_keyboard)
            bot.register_next_step_handler(message, callback=set_notification)

    except AttributeError:
        bot.send_message(message.chat.id, 'i dont understand, sorry bro', reply_markup=back_button_keyboard)
        bot.register_next_step_handler(message, callback=set_notification)


# def send_notification(user_id: int, cron_date: str):
#   pass


'''                                            
########################################################################################################################
NOTIFICATION FUNCTION END
########################################################################################################################                                                                 
'''

'''
########################################################################################################################
GROUP NAME CHANGE
########################################################################################################################                                                                 
'''


@bot.message_handler(content_types=['text'])
def change_group_name(message):
    try:

        if message.text == back_button:
            bot.send_message(message.chat.id, 'Возвращаюсь назад...',
                             reply_markup=settings_menu_keyboard)
            bot.register_next_step_handler(message, callback=settings_menu)

        elif message.text.lower() == db.get_group_name_by_id(message.chat.id)[0].lower():
            bot.send_sticker(message.chat.id,
                             'CAACAgIAAxkBAAEB0mZgEfH5yOePEH_hLh0Op31xUEzkRwAC3QIAAhly1DQ5KcCTEWI3Ax4E')
            bot.send_message(message.chat.id, 'Простите, но мне кажется Вы уже и так залогинены под группой'
                                              ' <b>{}</b> 🤨'.format(message.text),
                             parse_mode='HTML', reply_markup=back_button_keyboard)
            bot.register_next_step_handler(message, callback=change_group_name)

        elif Schedule.is_group_exist(message.text):
            db.users_update_group_name(message.from_user.username, message.text.upper(), time.strftime('%d/%m/%y, %X'),
                                       message.chat.id)
            bot.send_message(message.chat.id, 'Теперь Вы залогинены под группой <b>{}</b>.'.
                             format(db.get_group_name_by_id(message.chat.id)[0]),
                             parse_mode='HTML', reply_markup=main_menu_keyboard)
            bot.register_next_step_handler(message, callback=main_menu)

            global links_inline_subjects_keyboard, w, w_dict
            links_inline_subjects_keyboard = telebot.types.InlineKeyboardMarkup()

            w = []
            w_dict = {}

            list_subjects = list(Schedule.get_lessons(message.chat.id))
            len_list_subjects = len(Schedule.get_lessons(message.chat.id))
            len_subjects = 0
            for subject in list_subjects:
                len_subjects += 1
                w.append(subject)
                w_dict[subject[:15]] = subject

                if len_subjects < len_list_subjects + 1:
                    links_inline_subjects_keyboard.add(
                        telebot.types.InlineKeyboardButton(text=subject, callback_data='{}'.format(subject[:15])))

            links_inline_subjects_keyboard.add(
                telebot.types.InlineKeyboardButton(text='Назад', callback_data='first_back_button'),
                in_main_menu_inline_button)

        else:
            bot.send_message(message.chat.id, '<b>{}</b>? Я о такой группе пока-что не слышал. Попробуй ещё раз.'
                                              '\nПример: <b>IO-83</b>'.format(message.text),
                             parse_mode='HTML', reply_markup=back_button_keyboard)
            bot.register_next_step_handler(message, callback=change_group_name)

    except AttributeError:
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEB0mpgEfSs5sWQJ-AhnFT8wBbS_wd29gACkgADN4B1OuUYBW3X7hEZHgQ',
                         reply_markup=back_button_keyboard)
        bot.register_next_step_handler(message, callback=change_group_name)


'''                                            
########################################################################################################################
GROUP NAME CHANGE END
########################################################################################################################                                                                 
'''

if __name__ == '__main__':
    bot.polling()