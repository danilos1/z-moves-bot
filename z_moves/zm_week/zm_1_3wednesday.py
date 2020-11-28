from z_moves import zm_llp_list, zm_global_links, zm_hotlines

ZM_skeleton = '''
Запланированные мувы на среду:
———————————————
08:30 — {lesson1}
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
'''.format(lesson1=zm_llp_list.SP_lab_Pavlov, lesson2=zm_llp_list.OPP_lec_Korochkin,
           lesson3=zm_llp_list.OPP_lab_Korochkin, lesson4=zm_llp_list.KS_lab_Verba, hotlines=zm_hotlines.hotlines,
           global_links=zm_global_links.global_links, afterword="")

