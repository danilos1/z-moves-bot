from z_moves.scripts.schedule_parser import *

schedule = Schedule()
schedule.url_for_teachers = schedule.url_for_teachers.format('Верба Олександр Андрійович')
print(schedule.get_day_for_teacher(1, 2))
