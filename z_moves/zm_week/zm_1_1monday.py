from z_moves import zm_global_links, zm_hotlines

ZM_skeleton = '''
Запланированные мувы на понедельник:
———————————————
АДИХАЕМ
———————————————
{hotlines}
———————————————
{global_links}
———————————————
{afterword}
'''.format(hotlines=zm_hotlines.hotlines, global_links=zm_global_links.
           global_links, afterword="")

