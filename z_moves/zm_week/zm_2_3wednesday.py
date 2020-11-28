from z_moves import zm_llp_list, zm_global_links, zm_hotlines

ZM_skeleton = '''
Запланированные мувы на среду:
———————————————
10:25 — {lesson2}
———————————————
{hotlines}
———————————————
{global_links}
———————————————
{afterword}
'''.format(lesson2=zm_llp_list.OPP_lec_Korochkin, hotlines=zm_hotlines.hotlines,
           global_links=zm_global_links.global_links, afterword="")

