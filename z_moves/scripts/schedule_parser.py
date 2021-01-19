import requests
from bs4 import BeautifulSoup
import z_moves.scripts.session_db as sdb
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
url_for_students_pattern = 'http://api.rozklad.org.ua/v2/groups/{0}/lessons'
url_for_teachers_pattern = 'http://api.rozklad.org.ua/v2/teachers/{0}/lessons'

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


def get_links(user_id):
    links = db.get_links_by_id(user_id)
    links_text = ''
    if len(links) == 0:
        links_text = 'Вы еще не добавили ни одной ссылки.\nДля занесения ссылки перейдите в настройки ⚙'
    else:
        for l in links:
            HL = 'ℹ️  <a href="{link}">{text}</a>\n'
            links_text += HL.format(link=l[0], text=l[1])

    return links_text

def get_user_role(user_id):
    user_role = db.get_user_role_by_id(user_id)
    user_role_text = ''
    if len(user_role) == 0:
        user_role_text = 'PUSTO'
    else:
        for l in user_role:
            HL = '{user_role}'
            user_role_text += HL.format(user_role=l[0])

    return user_role_text

def get_user_name(user_id):
    user_name = db.get_user_name_by_id(user_id)
    user_name_text = ''
    if len(user_name) == 0:
        user_name_text = 'PUSTO'
    else:
        for l in user_name:
            HL = '{user_name}'
            user_name_text += HL.format(user_name=l[0])

    return user_name_text

def get_mails(user_id):
    mails = db.get_mails_by_id(user_id)
    mails_text = ''
    if len(mails) == 0:
        mails_text = 'nema! :('
    else:
        for d in mails:
            HL = 'ℹ️  <a href="{link}">{text}</a>\n'
            mails_text += HL.format(link=d[0], text=d[1])

    return mails_text

def get_hotlines(user_id):
    hotlines = db.get_hotline_by_id(user_id)
    hotline_text = ''
    if len(hotlines) == 0:
        hotline_text = 'На текущий момент я не наблюдаю хотлайнов ☺️.\nДля занесения хотлайна перейдите в настройки ⚙'
    else:
        for h in hotlines:
            HL = ' <a href="{link}">{text}</a>\n'
            hotline_text += h[0] + ' — ' + h[1] + ' — ' + h[2] + HL.format(link=h[3], text=' ℹ️')

    return hotline_text


def get_current_week():
    weekUrl = 'http://api.rozklad.org.ua/v2/weeks'
    week = requests.get(weekUrl).json()['data']
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


def show_exams(sch: str):
    return '''Запланированные мувы на экзамены: 
———————————————
{schedule}
———————————————
'''.format(schedule=sch)


class Schedule:
    role: str
    url: str
    id: str

    @staticmethod
    def is_teacher_exist(name: str):
        url = url_for_teachers_pattern
        return requests.get(url.format(name)).ok

    @staticmethod
    def is_group_exist(group: str):
        url = url_for_students_pattern
        return requests.get(url.format(group)).ok

    def get_schedule(self, week, day):
        schedule = ''
        if self.role == 'студент':
            r = requests.get(self.url)
            data = r.json()['data']
            for lesson in data:
                if lesson['lesson_week'] == str(week) and lesson['day_number'] == str(day):
                    lessonStart = lesson["time_start"][:5]
                    schedule += '\n' + str(lesson_numbers.get(lessonStart)) + ' ' + lessonStart + ' — <i>' + \
                                lesson["lesson_name"] + '</i> <b>\n' + \
                                lesson["lesson_type"] + "</b> — " + \
                                lesson["teacher_name"] + '\n'

        elif self.role == 'преподаватель':
            r = requests.get(self.url)
            data = r.json()['data']
            for lesson in data:
                if lesson['lesson_week'] == str(week) and lesson['day_number'] == str(day):
                    lessonStart = lesson["time_start"][:5]
                    schedule += '\n' + str(lesson_numbers.get(lessonStart)) + ' ' + lessonStart + ' — <i>' + \
                                lesson["lesson_name"] + '</i> \n<b>' + \
                                lesson["lesson_type"] + "</b> — " + \
                                lesson["teacher_name"] + '\n'

                    group_list = []
                    for group in lesson['groups']:
                        group_list.append(group['group_full_name'])
                    schedule += 'Груп' + ('а: ' if len(group_list) == 1 else 'и: ') + ', '.join(group_list) + '\n'
        else:
            schedule = 'Не удаётся вас распознать'

        return free if (schedule == '') else schedule

    @staticmethod
    def get_teacher_name(full_name: str):
        name = full_name.split(' ')
        return name[1] + ' ' + name[2]

    def identify_as(self, role: str, id: str):
        if role == 'студент':
            self.url = url_for_students_pattern
        elif role == 'преподаватель':
            self.url = url_for_teachers_pattern
        else:
            raise AttributeError('Cannot identify your role')

        self.id = id
        self.url = self.url.format(id)
        self.role = role

    def get_session_for_schedule(self):
        full_url = session_url + sdb.session_tokens[self.id]
        req = requests.get(full_url)
        soup = BeautifulSoup(req.content, 'html.parser')

        trS = []
        rows = soup.find_all('tr')
        schedule = ''
        for row in rows:
            trS.append(row.find_all('td'))

        i = 0
        for td in trS:
            if td[1].getText():
                schedule += '\n⚠️<b>' + td[0].getText() + '</b>\n' + subject_enumeration[i] + ' '
                for link in td[1].find_all('a', href=True):
                    schedule += '\n' + link.getText()
                schedule += ' : ' + td[1].getText()[-5:] + '\n'
                i += 1

        return show_exams(schedule)
