import requests

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


def show_schedule(sch: str, hl: str, gl: str, aw: str):
    return '''
Запланированные мувы на понедельник:
——————————————————————————————
{schedule}
——————————————————————————————
{hotlines}
——————————————————————————————
{global_links}
——————————————————————————————
{afterword}
'''.format(schedule=sch, hotlines=hl, global_links=gl, afterword=aw)


class Schedule:
    url = 'http://api.rozklad.org.ua/v2/groups/{0}/lessons'

    def is_group_exist(self, group: str):
        return requests.get(self.url.format(group)).ok

    def getDay(self, week, day):
        schedule = ''
        r = requests.get(self.url)
        data = r.json()['data']
        for lesson in data:
            if lesson['lesson_week'] == str(week) and lesson['day_number'] == str(day):
                schedule += '\n' + lesson["time_start"][:5] + ' — <i>' + \
                            lesson["lesson_name"] + '</i> <b>' + \
                            lesson["lesson_type"] + "</b> — " + \
                            lesson["teacher_name"]

        return free if (schedule == '') else schedule
