from z_moves import zm_llp_list, zm_global_links, zm_hotlines

ZM_skeleton = '''
Запланированные мувы на четверг:
———————————————
10:25 — {lesson2}
———————————————
12:20 — {lesson3}
———————————————
14:15 — {lesson4}
———————————————
{hotlines}
———————————————
{global_links}
———————————————
{afterword}
'''.format(lesson2=zm_llp_list.AK_lec_Klymenko, lesson3=zm_llp_list.KM_lab_Radchenko,
           lesson4=zm_llp_list.English_prak_Hrabovska, hotlines=zm_hotlines.hotlines,
           global_links=zm_global_links.global_links, afterword="")

