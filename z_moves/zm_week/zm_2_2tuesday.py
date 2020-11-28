from z_moves import zm_llp_list, zm_global_links, zm_hotlines

ZM_skeleton = '''
Запланированные мувы на вторник:
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
'''.format(lesson2=zm_llp_list.KS_lec_Verba, lesson3=zm_llp_list.SP_lec_Pavlov, hotlines=zm_hotlines.hotlines,
           global_links=zm_global_links.global_links, afterword="")

