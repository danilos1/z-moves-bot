from z_moves.scripts.schedule_parser import get_current_week
from datetime import date
import telebot

current_week = get_current_week()
current_day = date.today().weekday()

# main menu buttons
schedule_button = '📆 Расписание'
settings_button = '⚙ Настройки'
hotlines_button = '👺 Хотлайны'
links_button = '🔗 Ссылки'
mails_button = '✉️ Почты'
info_button = 'ℹ️Инфо'
help_button = '❓ Помощь'

links_inline_add_button = telebot.types.InlineKeyboardButton(text='Добавить ссылку', callback_data='add_link')
links_inline_change_button = telebot.types.InlineKeyboardButton(text='Изменить ссылку', callback_data='change_link')
links_inline_remove_button = telebot.types.InlineKeyboardButton(text='Удалить ссылку', callback_data='remove_link')

links_inline_lec_button = telebot.types.InlineKeyboardButton(text='Лек', callback_data='labwork')
links_inline_lab_button = telebot.types.InlineKeyboardButton(text='Лаб', callback_data='lecture')
links_inline_practice_button = telebot.types.InlineKeyboardButton(text='Прак', callback_data='practice')

# main menu instant replies
info_button_reply = '<b>Z-Moves Bot</b>\n\nВы авторизованы под группой: <b>{0}</b>'
help_button_reply = '<b>Что может бот ?</b>\n\nНихуя.'

# schedule menu buttons
today_day_button = "📝 Расписание на сегодня"
tomorrow_day_button = "📝 Расписание на завтра"
week1_button = '1️⃣ Неделя ✅' if current_week == 1 else '1️⃣ Неделя'
week2_button = '2️⃣ Неделя ✅' if current_week == 2 else '2️⃣ Неделя'
day_button = [
    '🤯 Пн' + (' ✅' if current_day == 0 else ''),
    '😫 Вт' + (' ✅' if current_day == 1 else ''),
    '😞 Ср' + (' ✅' if current_day == 2 else ''),
    '😏 Чт' + (' ✅' if current_day == 3 else ''),
    '🤤 Пт' + (' ✅' if current_day == 4 else '')
]

# settings menu buttons
add_link_button = '🔗 Добавить ссылку'
add_hotline_button = '👺 Добавить хотлайны'
add_mail_button = '✉️ Добавить почту'
notification_button = '🔕 Уведомления'
change_group_name_button = '‍🔧 Изменить группу'

# global back button
back_button = '⬅️Назад'
inline_back_button = telebot.types.InlineKeyboardButton(text='Назад', callback_data='back_button')
inline_step_back_button = telebot.types.InlineKeyboardButton(text='Назад', callback_data='step_back_button')

# reply of not available bot functions
not_available_reply = '⛔ В разработке'

# test button
test_button = 'test'
