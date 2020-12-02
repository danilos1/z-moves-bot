import telebot
import os
from z_moves.buttons import *
from z_moves.scripts.schedule_parser import *


bot = telebot.TeleBot(os.environ['BOT_TOKEN'])
schedule = Schedule()

'''
########################################################################################################################
                                              REPLY_MARKUP= SECTION
########################################################################################################################                               
'''

back_button_keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
back_button_keyboard.add(back_button)

settings_keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
settings_keyboard.add(links_button, hotlines_button)
settings_keyboard.add(notifications_button, change_group_button)
settings_keyboard.add(back_button)

main_menu_keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
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
                                     REPLY_MARKUP= SECTION HAVE ENDED
########################################################################################################################
'''

'''
########################################################################################################################
                                                BOT START
########################################################################################################################
'''


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, '''
О, привет! 🥴🤙
Z-Moves на связи 😎

Для начала напиши мне из какой ты группы 🙂
''')
    bot.register_next_step_handler(message, callback=registration)


@bot.message_handler(content_types=['text'])
def registration(message):
    mtl = message.text.lower()
    if schedule.is_group_exist(mtl):
        schedule.url = schedule.url.format(mtl)
        bot.send_message(message.chat.id, 'Есть такая! Ну а теперь приступим 🙂', reply_markup=main_menu_keyboard)
        bot.register_next_step_handler(message, callback=main_menu)
    else:
        bot.send_message(message.chat.id, '''Ой, что-то я о такой не слышал 🤥\nПоробуй ещё''')


'''
########################################################################################################################
                                      BOT START PROCEDURE HAVE ENDED
########################################################################################################################
'''

'''                        
########################################################################################################################                    
                                                 MAIN MENU TREE       
########################################################################################################################                                                       
'''


@bot.message_handler(content_types=['text'])
def main_menu(message):
    mtl = message.text.lower()
    if mtl == schedule_button.lower():
        bot.send_message(message.chat.id, 'Выбери неделю', reply_markup=week_choose_keyboard)
        bot.register_next_step_handler(message, callback=week_choose)
    elif mtl == settings_button.lower():
        bot.send_message(message.chat.id, 'Что ты желаешь настроить?', reply_markup=settings_keyboard)
        bot.register_next_step_handler(message, callback=settings)
    elif mtl == info_button.lower():
        bot.send_message(message.chat.id, develop_button, reply_markup=main_menu_keyboard)
        bot.register_next_step_handler(message, callback=main_menu)
    elif mtl == help_button.lower():
        bot.send_message(message.chat.id, develop_button, reply_markup=main_menu_keyboard)
        bot.register_next_step_handler(message, callback=main_menu)


'''                        
########################################################################################################################
                                            MAIN MENU TREE HAVE ENDED      
########################################################################################################################
'''

'''
########################################################################################################################                                            
                                                  SCHEDULE BRANCH                   
########################################################################################################################                                                  
'''


@bot.message_handler(content_types=['text'])
def week_choose(message):
    mtl = message.text.lower()
    if mtl == week1_button.lower():
        bot.send_message(message.chat.id, 'А теперь день', reply_markup=day_choose_keyboard)
        bot.register_next_step_handler(message, callback=week_1)
    elif mtl == week2_button.lower():
        bot.send_message(message.chat.id, 'А теперь день', reply_markup=day_choose_keyboard)
        bot.register_next_step_handler(message, callback=week_2)
    elif mtl == back_button.lower():
        bot.send_message(message.chat.id, 'Возвращаемся...', reply_markup=main_menu_keyboard)
        bot.register_next_step_handler(message, callback=main_menu)


@bot.message_handler(content_types=['text'])
def week_1(message):
    mtl = message.text.lower()

    if mtl == day_button[0].lower():
        bot.send_message(message.chat.id, show_schedule(week_days[0], schedule.getDay(1, 1), '', '', ''),
                         parse_mode="HTML",
                         reply_markup=day_choose_keyboard)
        bot.register_next_step_handler(message, callback=week_1)

    if mtl == day_button[1].lower():
        bot.send_message(message.chat.id, show_schedule(week_days[1], schedule.getDay(1, 2), '', '', ''),
                         parse_mode="HTML",
                         reply_markup=day_choose_keyboard)
        bot.register_next_step_handler(message, callback=week_1)

    if mtl == day_button[2].lower():
        bot.send_message(message.chat.id, show_schedule(week_days[2], schedule.getDay(1, 3), '', '', ''),
                         parse_mode="HTML",
                         reply_markup=day_choose_keyboard)
        bot.register_next_step_handler(message, callback=week_1)

    if mtl == day_button[3].lower():
        bot.send_message(message.chat.id, show_schedule(week_days[3], schedule.getDay(1, 4), '', '', ''),
                         parse_mode="HTML",
                         reply_markup=day_choose_keyboard)
        bot.register_next_step_handler(message, callback=week_1)

    if mtl == day_button[4].lower():
        bot.send_message(message.chat.id, show_schedule(week_days[4], schedule.getDay(1, 5), '', '', ''),
                         parse_mode="HTML",
                         reply_markup=day_choose_keyboard)
        bot.register_next_step_handler(message, callback=week_1)

    if mtl == back_button.lower():
        bot.send_message(message.chat.id,
                         text='Возвращаемся назад...',
                         reply_markup=week_choose_keyboard)
        bot.register_next_step_handler(message, callback=week_choose)


@bot.message_handler(content_types=['text'])
def week_2(message):
    mtl = message.text.lower()

    if mtl == day_button[0].lower():
        bot.send_message(message.chat.id, show_schedule(week_days[0], schedule.getDay(2, 1), '', '', ''),
                         parse_mode="HTML",
                         reply_markup=day_choose_keyboard)
        bot.register_next_step_handler(message, callback=week_2)

    if mtl == day_button[1].lower():
        bot.send_message(message.chat.id, show_schedule(week_days[1], schedule.getDay(2, 2), '', '', ''),
                         parse_mode="HTML",
                         reply_markup=day_choose_keyboard)
        bot.register_next_step_handler(message, callback=week_2)

    if mtl == day_button[2].lower():
        bot.send_message(message.chat.id, show_schedule(week_days[2], schedule.getDay(2, 3), '', '', ''),
                         parse_mode="HTML",
                         reply_markup=day_choose_keyboard)
        bot.register_next_step_handler(message, callback=week_2)

    if mtl == day_button[3].lower():
        bot.send_message(message.chat.id, show_schedule(week_days[3], schedule.getDay(2, 4), '', '', ''),
                         parse_mode="HTML",
                         reply_markup=day_choose_keyboard)
        bot.register_next_step_handler(message, callback=week_2)

    if mtl == day_button[4].lower():
        bot.send_message(message.chat.id, show_schedule(week_days[4], schedule.getDay(2, 5), '', '', ''),
                         parse_mode="HTML",
                         reply_markup=day_choose_keyboard)
        bot.register_next_step_handler(message, callback=week_2)

    if mtl == back_button.lower():
        bot.send_message(message.chat.id,
                         text='Возвращаемся назад...',
                         reply_markup=week_choose_keyboard)
        bot.register_next_step_handler(message, callback=week_choose)


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
    mtl = message.text.lower()
    if mtl == links_button.lower():
        bot.send_message(message.chat.id, develop_button, reply_markup=settings_keyboard)
        bot.register_next_step_handler(message, settings)
    elif mtl == hotlines_button.lower():
        bot.send_message(message.chat.id, develop_button, reply_markup=settings_keyboard)
        bot.register_next_step_handler(message, settings)
    elif mtl == notifications_button.lower():
        bot.send_message(message.chat.id, develop_button, reply_markup=settings_keyboard)
        bot.register_next_step_handler(message, settings)
    elif mtl == change_group_button.lower():
        bot.send_message(message.chat.id, develop_button, reply_markup=settings_keyboard)
        bot.register_next_step_handler(message, settings)
    elif mtl == back_button.lower():
        bot.send_message(message.chat.id, 'Возвращаемся...', reply_markup=main_menu_keyboard)
        bot.register_next_step_handler(message, callback=main_menu)


bot.polling()
