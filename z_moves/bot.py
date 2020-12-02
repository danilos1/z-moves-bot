import telebot
from z_moves.scripts.schedule_parser import *
from z_moves.zm_week import zm_1_2tuesday, zm_1_5friday, zm_2_1monday, zm_2_5friday, zm_2_2tuesday, zm_2_4thursday, \
    zm_1_1monday, zm_2_3wednesday, zm_1_4thursday
from z_moves.buttons import *

bot = telebot.TeleBot('1469473212:AAGdm_vV4vuwfD0qXfwAq-4If7eI4sjWQFA')
schedule = Schedule()

'''
########################################################################################################################
                                              REPLY_MARKUP= SECTION
########################################################################################################################                               
'''

BackButtonKeyboard = telebot.types.ReplyKeyboardMarkup(True, True)
BackButtonKeyboard.add('⬅️Назад')

SettingsKeyboard = telebot.types.ReplyKeyboardMarkup(True, True)
SettingsKeyboard.add('🔗 Ссылки', '👺 Хотлайны')
SettingsKeyboard.add('📢 Уведомления', '‍🎓 Группа')
SettingsKeyboard.add('⬅ Назад')

StartKeyboard = telebot.types.ReplyKeyboardMarkup(True, True)
StartKeyboard.add('📆 Расписание', '⚙ Настройки')
StartKeyboard.add('ℹ Инфо', '❓ Помощь')

keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard1.add(week1_button, week2_button)
keyboard1.add('⬅ Назад')

keyboard2 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard2.add('🤯 Пн', '😫 Вт', '😞 Ср', '😏 Чт', '🤤 Пт', '⬅ Назад')

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
    text = message.text.lower()
    if schedule.is_group_exist(text):
        schedule.url = schedule.url.format(text)
        bot.send_message(message.chat.id, 'Есть такая! Ну а теперь приступим 🙂', reply_markup=StartKeyboard)
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
    if message.text.lower() == '📆 расписание':
        bot.send_message(message.chat.id, 'Выбери неделю', reply_markup=keyboard1)
        bot.register_next_step_handler(message, callback=week_choose)
    elif message.text.lower() == '⚙ настройки':
        bot.send_message(message.chat.id, 'Что ты желаешь настроить?', reply_markup=SettingsKeyboard)
        bot.register_next_step_handler(message, callback=settings)
    elif message.text.lower() == 'ℹ инфо':
        bot.send_message(message.chat.id, '⛔ В разработке', reply_markup=StartKeyboard)
        bot.register_next_step_handler(message, callback=main_menu)
    elif message.text.lower() == '❓ помощь':
        bot.send_message(message.chat.id, '⛔ В разработке', reply_markup=StartKeyboard)
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
    if message.text.lower() == week1_button.lower():
        bot.send_message(message.chat.id, 'А теперь день', reply_markup=keyboard2)
        bot.register_next_step_handler(message, callback=week_1)
    elif message.text.lower() == week2_button.lower():
        bot.send_message(message.chat.id, 'А теперь день', reply_markup=keyboard2)
        bot.register_next_step_handler(message, callback=week_2)
    elif message.text.lower() == '⬅ назад':
        bot.send_message(message.chat.id, 'Возвращаемся...', reply_markup=StartKeyboard)
        bot.register_next_step_handler(message, callback=main_menu)


@bot.message_handler(content_types=['text'])
def week_1(message):
    if message.text.lower() == '🤯 пн':
        bot.send_message(message.chat.id, show_schedule(schedule.getDay(1, 1), '', '', ''), parse_mode="HTML",
                         reply_markup=keyboard2)
        bot.register_next_step_handler(message, callback=week_1)
    if message.text.lower() == '😫 вт':
        bot.send_message(message.chat.id, show_schedule(schedule.getDay(1, 2), '', '', ''), parse_mode="HTML",
                         reply_markup=keyboard2)
        bot.register_next_step_handler(message, callback=week_1)
    if message.text.lower() == '😞 ср':
        bot.send_message(message.chat.id, show_schedule(schedule.getDay(1, 3), '', '', ''), parse_mode="HTML",
                         reply_markup=keyboard2)
        bot.register_next_step_handler(message, callback=week_1)
    if message.text.lower() == '😏 чт':
        bot.send_message(message.chat.id, show_schedule(schedule.getDay(1, 4), '', '', ''), parse_mode="HTML",
                         reply_markup=keyboard2)
        bot.register_next_step_handler(message, callback=week_1)
    if message.text.lower() == '🤤 пт':
        bot.send_message(message.chat.id, show_schedule(schedule.getDay(1, 5), '', '', ''), parse_mode="HTML",
                         reply_markup=keyboard2)
        bot.register_next_step_handler(message, callback=week_1)
    if message.text.lower() == '⬅ назад':
        bot.send_message(message.chat.id, text='Возвращаемся назад...', reply_markup=keyboard1)
        bot.register_next_step_handler(message, callback=week_choose)


@bot.message_handler(content_types=['text'])
def week_2(message):
    if message.text.lower() == '🤯 пн':
        bot.send_message(message.chat.id, zm_2_1monday.ZM_skeleton, parse_mode="HTML", reply_markup=keyboard2)
        bot.register_next_step_handler(message, callback=week_2)
    if message.text.lower() == '😫 вт':
        bot.send_message(message.chat.id, zm_2_2tuesday.ZM_skeleton, parse_mode="HTML", reply_markup=keyboard2)
        bot.register_next_step_handler(message, callback=week_2)
    if message.text.lower() == '😞 ср':
        bot.send_message(message.chat.id, zm_2_3wednesday.ZM_skeleton, parse_mode="HTML", reply_markup=keyboard2)
        bot.register_next_step_handler(message, callback=week_2)
    if message.text.lower() == '😏 чт':
        bot.send_message(message.chat.id, zm_2_4thursday.ZM_skeleton, parse_mode="HTML", reply_markup=keyboard2)
        bot.register_next_step_handler(message, callback=week_2)
    if message.text.lower() == '🤤 пт':
        bot.send_message(message.chat.id, zm_2_5friday.ZM_skeleton, parse_mode="HTML", reply_markup=keyboard2)
        bot.register_next_step_handler(message, callback=week_2)
    if message.text.lower() == '⬅ назад':
        bot.send_message(message.chat.id, text='Возвращаемся назад...', reply_markup=keyboard1)
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
    msg = message.text.lower()
    if msg == '🔗 ссылки':
        bot.send_message(message.chat.id, '⛔️ В разработке', reply_markup=SettingsKeyboard)
        bot.register_next_step_handler(message, settings)
    elif msg == '👺 хотлайны':
        bot.send_message(message.chat.id, '⛔️ В разработке/ WAIT NAHOOI', reply_markup=SettingsKeyboard)
        bot.register_next_step_handler(message, settings)
    elif msg == '📢 уведомления':
        bot.send_message(message.chat.id, '⛔️ В разработке', reply_markup=SettingsKeyboard)
        bot.register_next_step_handler(message, settings)
    elif msg == '‍🎓 группа':
        bot.send_message(message.chat.id, '⛔️ В разработке', reply_markup=SettingsKeyboard)
        bot.register_next_step_handler(message, settings)
    elif msg == '⬅ назад':
        bot.send_message(message.chat.id, 'Возвращаемся...', reply_markup=StartKeyboard)
        bot.register_next_step_handler(message, callback=main_menu)


bot.polling()
