import telebot
from z_moves.zm_week import zm_1_3wednesday
from z_moves.zm_week import zm_1_2tuesday, zm_1_5friday, zm_2_1monday, zm_2_5friday, zm_2_2tuesday, zm_2_4thursday, \
    zm_1_1monday, zm_2_3wednesday, zm_1_4thursday

bot = telebot.TeleBot('1469473212:AAGdm_vV4vuwfD0qXfwAq-4If7eI4sjWQFA')

print("bot-huebot")


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
keyboard1.add('1️⃣ Неделя', '2️⃣ Неделя')
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
    if message.text.lower() == 'io83' or message.text.lower() == 'io-83' or message.text.lower() == 'іо83' or \
       message.text.lower() == 'іо-83' or message.text.lower() == 'ио83' or message.text.lower() == 'ио-83':

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
    if message.text.lower() == '1️⃣ неделя':
        bot.send_message(message.chat.id, 'А теперь день', reply_markup=keyboard2)
        bot.register_next_step_handler(message, callback=week_1)
    elif message.text.lower() == '2️⃣ неделя':
        bot.send_message(message.chat.id, 'А теперь день', reply_markup=keyboard2)
        bot.register_next_step_handler(message, callback=week_2)
    elif message.text.lower() == '⬅ назад':
        bot.send_message(message.chat.id, 'Возвращаемся...', reply_markup=StartKeyboard)
        bot.register_next_step_handler(message, callback=main_menu)


@bot.message_handler(content_types=['text'])
def week_1(message):
    if message.text.lower() == '🤯 пн':
        bot.send_message(message.chat.id, zm_1_1monday.ZM_skeleton, parse_mode="HTML", reply_markup=keyboard2)
        bot.register_next_step_handler(message, callback=week_1)
    if message.text.lower() == '😫 вт':
        bot.send_message(message.chat.id, zm_1_2tuesday.ZM_skeleton, parse_mode="HTML", reply_markup=keyboard2)
        bot.register_next_step_handler(message, callback=week_1)
    if message.text.lower() == '😞 ср':
        bot.send_message(message.chat.id, zm_1_3wednesday.ZM_skeleton, parse_mode="HTML", reply_markup=keyboard2)
        bot.register_next_step_handler(message, callback=week_1)
    if message.text.lower() == '😏 чт':
        bot.send_message(message.chat.id, zm_1_4thursday.ZM_skeleton, parse_mode="HTML", reply_markup=keyboard2)
        bot.register_next_step_handler(message, callback=week_1)
    if message.text.lower() == '🤤 пт':
        bot.send_message(message.chat.id, zm_1_5friday.ZM_skeleton, parse_mode="HTML", reply_markup=keyboard2)
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
    if message.text.lower() == '🔗 ссылки':
        bot.send_message(message.chat.id, '⛔️ В разработке', reply_markup=SettingsKeyboard)
        bot.register_next_step_handler(message, settings)
    elif message.text.lower() == '👺 хотлайны':
        bot.send_message(message.chat.id, '⛔️ В разработке/ WAIT NAHOOI', reply_markup=SettingsKeyboard)
        bot.register_next_step_handler(message, settings)
    elif message.text.lower() == '📢 уведомления':
        bot.send_message(message.chat.id, '⛔️ В разработке', reply_markup=SettingsKeyboard)
        bot.register_next_step_handler(message, settings)
    elif message.text.lower() == '‍🎓 группа':
        bot.send_message(message.chat.id, '⛔️ В разработке', reply_markup=SettingsKeyboard)
        bot.register_next_step_handler(message, settings)
    elif message.text.lower() == '⬅ назад':
        bot.send_message(message.chat.id, 'Возвращаемся...', reply_markup=StartKeyboard)
        bot.register_next_step_handler(message, callback=main_menu)


bot.polling()
