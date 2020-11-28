from z_moves import zm_llp_list, zm_global_links, zm_hotlines

ZM_skeleton = '''
Запланированные мувы на пятницу:
———————————————
10:25 — {lesson2}
———————————————
12:20 — {lesson3}
———————————————
{hotlines}
———————————————
{global_links}
———————————————
{afterword}
'''.format(lesson2=zm_llp_list.KM_lec_Radchenko, lesson3=zm_llp_list.SOS_lec_Vinogradov, hotlines=zm_hotlines.hotlines,
           global_links=zm_global_links.global_links, afterword="")
