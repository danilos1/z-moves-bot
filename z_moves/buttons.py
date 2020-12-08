from z_moves.scripts.schedule_parser import *

current_week = get_current_week()
current_day = date.today().weekday()

week1_button = '1️⃣ Неделя ✅' if current_week == 1 else '1️⃣ Неделя'
week2_button = '2️⃣ Неделя ✅' if current_week == 2 else '2️⃣ Неделя'

student_button = '🎓 Студент'
teacher_button = '🎓 Преподаватель'

back_button = '⬅️Назад'

links_button = '🔗 Ссылки'
hotlines_button = '👺 Хотлайны'
notifications_button = '🔕 Уведомления'
change_group_button = '‍🎓 Перерегистрироваться'

current_day_button = "📝 Текущее расписание"
tomorrow_day_button = "📝 Расписание на завтра"
schedule_button = '📆 Расписание'
settings_button = '⚙ Настройки'
##################################
info_button = 'ℹ Инфо'
help_button = '❓ Помощь'
#################################
day_button = [
    '🤯 Пн'+(' ✅' if current_day == 0 else ''),
    '😫 Вт'+(' ✅' if current_day == 1 else ''),
    '😞 Ср'+(' ✅' if current_day == 2 else ''),
    '😏 Чт'+(' ✅' if current_day == 3 else ''),
    '🤤 Пт'+(' ✅' if current_day == 4 else '')
]

develop_button = '⛔ В разработке'
















