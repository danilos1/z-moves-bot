from bot.backend.schedule_parser import Database


def is_exist(groupName):
    return groupName in Database.groups


class ScheduleParser:

    def __init__(self, groupName):
        self.groupName = groupName
