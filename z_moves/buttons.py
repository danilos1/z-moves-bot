from z_moves.scripts.schedule_parser import get_current_week
from datetime import date

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

# reply of not available bot functions
not_available_reply = '⛔ В разработке'

# test button

test_button = 'test'