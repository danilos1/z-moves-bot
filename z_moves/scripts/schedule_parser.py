import requests
from bs4 import BeautifulSoup
import z_moves.scripts.db as db

free = '''
░░▄█████████████████▄
░▐████▀▒▒БОЛДАК▒▒▀████
░███▀▒▒▒РАЗРЕШИЛ▒▒▒▒▀██
░▐██▒▒▒▒▒АДИХНУТЬ▒▒▒▒▒██
░▐█▌▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒███
░░█▒▄▀▀▀▀▀▄▒▒▄▀▀▀▀▀▄▒▐██
░░░▐░░░▄▄░░▌▐░░░▄▄░░▌▐██
░▄▀▌░░░▀▀░░▌▐░░░▀▀░░▌▒▀▒
░▌▒▀▄░░░░▄▀▒▒▀▄░░░▄▀▒▒▄▀
░▀▄▐▒▀▀▀▀▒▒▒▒▒▒▀▀▀▒▒▒▒▒▒
░░░▀▌▒▄██▄▄▄▄████▄▒▒▒▒█▀
░░░░▄██████████████▒▒▐▌
░░░▀███▀▀████▀█████▀▒▌
░░░░░▌▒▒▒▄▒▒▒▄▒▒▒▒▒▒▐
░░░░░▌▒▒▒▒▀▀▀▒▒▒▒▒▒▒▐
'''

session_url = 'http://rozklad.kpi.ua/Schedules/ViewSessionSchedule.aspx?g='

week_days = {
    1: 'понедельник',
    2: 'вторник',
    3: 'среду',
    4: 'четверг',
    5: 'пятницу'
}

lesson_numbers = {
    '08:30': '1️⃣',
    '10:25': '2️⃣',
    '12:20': '3️⃣',
    '14:15': '4️⃣',
    '16:10': '5️⃣'
}

subject_enumeration = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣']


def show_exams(sch: str):
    return '''Запланированные мувы на экзамены: 	
———————————————	
{schedule}	
———————————————	
'''.format(schedule=sch)


def get_links(user_id):
    links = db.get_links_by_id(user_id)
    links_text = ''
    if len(links) == 0:
        links_text = 'Вы еще не добавили ни одной ссылки.\nДля занесения ссылки перейдите в настройки ⚙'
    else:
        for l in links:
            hl = '1️⃣️  <a href="{link}">{text}</a>\n'
            links_text += hl.format(link=l[0], text=l[1])

    return links_text


def get_mails(user_id):
    mails = db.get_mails_by_id(user_id)
    mails_text = ''
    if len(mails) == 0:
        mails_text = 'nema! :('
    else:
        for d in mails:
            hl = 'ℹ️  <a href="{link}">{text}</a>\n'
            mails_text += hl.format(link=d[0], text=d[1])

    return mails_text


def get_hotlines(user_id):
    hotlines = db.get_hotline_by_id(user_id)
    hotline_text = ''
    if len(hotlines) == 0:
        hotline_text = 'На текущий момент я не наблюдаю хотлайнов ☺️.\nДля занесения хотлайна перейдите в настройки ⚙'
    else:
        for h in hotlines:
            hl = ' <a href="{link}">{text}</a>\n'
            hotline_text += h[0] + ' — ' + h[1] + ' — ' + h[2] + hl.format(link=h[3], text=' 1️⃣ ️')

    return hotline_text


def get_current_week():
    week_url = 'http://api.rozklad.org.ua/v2/weeks'
    week = requests.get(week_url).json()['data']
    return week


def show_schedule(user_id, day: str, sch: str):
    hl = get_hotlines(user_id)

    return 'Запланированные мувы на ' + day + ':\n' + '''
———————————————
{schedule}
———————————————
👺 Hotlines: 
{hotlines}
———————————————
'''.format(schedule=sch, hotlines=hl)


class Schedule:
    url_for_students_pattern = 'http://api.rozklad.org.ua/v2/groups/{0}/lessons'

    @staticmethod
    def is_group_exist(group: str):
        url = Schedule.url_for_students_pattern
        return requests.get(url.format(group)).ok

    @staticmethod
    def get_schedule(user_id, week, day):
        schedule = ''
        user = db.get_group_name_by_id(user_id)
        url = Schedule.url_for_students_pattern
        r = requests.get(url.format(user[0]))
        data = r.json()['data']

        for lesson in data:
            if lesson['lesson_week'] == str(week) and lesson['day_number'] == str(day):
                lesson_start = lesson["time_start"][:5]
                schedule += '\n' + str(lesson_numbers.get(lesson_start)) + ' ' + lesson_start + ' — <i>' + \
                            lesson["lesson_name"] + '</i> <b>\n' + \
                            lesson["lesson_type"] + "</b> — " + \
                            lesson["teacher_name"] + '\n'

        return free if (schedule == '') else schedule

    @staticmethod
    def get_lessons(user_id):
        reply = []
        user = db.get_group_name_by_id(user_id)
        url = Schedule.url_for_students_pattern
        r = requests.get(url.format(user[0]))
        data = r.json()['data']

        for lesson in data:
            reply.append(lesson["lesson_full_name"])

        return set(reply)

    @staticmethod
    def get_session_for_schedule(user_id):
        user = db.get_group_name_by_id(user_id)
        url = 'http://api.rozklad.org.ua/v2/groups/{0}'
        r = requests.get(url.format(user[0]))
        data = r.json()['data']

        group_token = data["group_url"][data["group_url"].index("g="):]
        full_url = 'http://rozklad.kpi.ua/Schedules/ViewSessionSchedule.aspx?'+group_token

        req = requests.get(full_url)

        soup = BeautifulSoup(req.content, 'html.parser')

        trs = []
        rows = soup.find_all('tr')
        schedule = ''
        for row in rows:
            trs.append(row.find_all('td'))

        i = 0
        for td in trs:
            if td[1].getText():
                schedule += '\n⚠️<b>' + td[0].getText() + '</b>\n' + subject_enumeration[i] + ' '
                for link in td[1].find_all('a', href=True):
                    schedule += '\n' + link.getText()
                schedule += ' : ' + td[1].getText()[-5:] + '\n'
                i += 1

        return show_exams(schedule)